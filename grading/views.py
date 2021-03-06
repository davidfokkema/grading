import logging

from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Course, Student, Assignment, Report, Skills, Enrollment
from .forms import UploadReportForm, UploadReportAssessmentForm
from .blackboard import BlackBoardUvA, BlackBoardVU
from . import utils


logger = logging.getLogger('django')


class IndexView(generic.ListView):
    model = Course
    template_name = 'grading/index.html'


class CourseView(generic.DetailView):
    model = Course
    template_name = 'grading/course.html'


class ReportView(generic.DetailView):
    model = Assignment
    template_name = 'grading/report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)

        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        all_students = assignment.course.students.all()

        students = []
        for student in all_students:
            enrollment = Enrollment.objects.get(
                student=student, course=assignment.course)
            info = {'name': str(student),
                    'has_report': False,
                    'has_assessment': False,
                    'mark': None,
                    'is_active': enrollment.is_active,
                    'mail_is_sent': False}
            try:
                report = Report.objects.get(assignment=assignment,
                                            student=student)
            except Report.DoesNotExist:
                pass
            else:
                if report.report:
                    info['has_report'] = True
                    info['report_url'] = report.report.url
                if report.assessment:
                    info['has_assessment'] = True
                    info['assessment_url'] = report.assessment.url
                if report.mail_is_sent:
                    info['mail_is_sent'] = True
                info['mark'] = report.mark
            students.append(info)
        context['students'] = students
        return context


class SkillsView(generic.DetailView):
    model = Assignment
    template_name = 'grading/skills.html'

    def get_context_data(self, **kwargs):
        context = super(SkillsView, self).get_context_data(**kwargs)

        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        all_students = Student.objects.filter(course=assignment.course)

        students = []
        for student in all_students:
            enrollment = Enrollment.objects.get(
                student=student, course=assignment.course)
            info = {'name': str(student),
                    'has_assessment': False,
                    'mark': None,
                    'is_active': enrollment.is_active,
                    'mail_is_sent': False}
            try:
                skills = Skills.objects.get(assignment=assignment,
                                            student=student)
            except Skills.DoesNotExist:
                pass
            else:
                if skills.assessment:
                    info['has_assessment'] = True
                    info['assessment_url'] = skills.assessment.url
                if skills.mail_is_sent:
                    info['mail_is_sent'] = True
                info['mark'] = skills.mark
            students.append(info)
        context['students'] = students
        return context


def upload_report_view(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)

    if request.method == 'POST':
        form = UploadReportForm(request.POST, request.FILES)
        files = request.FILES.getlist('reports')
        if form.is_valid():
            added, updated, unknown = [], [], []
            logger.info("FILES %d: %s" %
                        (len(files), '\t'.join([str(u) for u in files])))
            for f in files:
                logger.info("Processing file %s" % f)
                try:
                    student = utils.get_student_from_filename(f.name)
                    try:
                        report = Report.objects.get(assignment=assignment,
                                                    student=student)
                        updated.append(student)
                    except Report.DoesNotExist:
                        report = Report(assignment=assignment, student=student)
                        added.append(student)
                    report.report = f
                    report.save()
                except utils.IdentificationError:
                    unknown.append(f.name)
            return render(request, 'grading/upload_reports_status.html',
                          {'assignment': assignment,
                           'added': added,
                           'updated': updated,
                           'unknown': unknown})
    else:
        form = UploadReportForm()

    return render(request, 'grading/upload_reports.html',
                  {'assignment': assignment, 'form': form})


def upload_report_assessment_view(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)

    if request.method == 'POST':
        form = UploadReportAssessmentForm(request.POST)
        if form.is_valid():
            added, updated, unknown = [], [], []
            url = form.cleaned_data['url']
            for sheet in utils.get_sheets_from_url(url):
                name = sheet['properties']['title']
                try:
                    student = utils.get_student_from_name(name)
                except utils.IdentificationError:
                    unknown.append(name)
                else:
                    gid = sheet['properties']['sheetId']
                    print(student, gid)
                    pdf = utils.get_pdf_from_sheet_url(url, gid)
                    added.append(student)
            return render(request, 'grading/upload_reports_status.html',
                          {'assignment': assignment,
                           'added': added,
                           'updated': updated,
                           'unknown': unknown})
    else:
        form = UploadReportAssessmentForm()

    return render(request, 'grading/upload_report_assessments.html',
                  {'assignment': assignment, 'form': form})


def refresh_student_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    username = course.account.user
    unsafe_password = course.account.unsafe_password
    if course.account.account_type == 'bb_uva':
        BlackBoard = BlackBoardUvA
    elif course.account.account_type == 'bb_vu':
        BlackBoard = BlackBoardVU
    bb = BlackBoard(username, unsafe_password)
    students = bb.get_student_list(course.course_id)

    for student in students:
        try:
            s = Student.objects.get(student_id=student['student_id'])
            student['status'] = 'known'
        except Student.DoesNotExist:
            student['status'] = 'new'
            s = Student(first_name=student['first_name'],
                        last_name=student['last_name'],
                        student_id=student['student_id'],
                        email=student['email'])
            s.save()

        if course in s.course_set.all():
            student['status'] += '- already registered'
        else:
            enroll = Enrollment(student=s, course=course)
            s.save()
            enroll.save()
            student['status'] += '- now registered'

    return render(request, 'grading/refresh_student_list.html',
                  {'course': course, 'students': students})
