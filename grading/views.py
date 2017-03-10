import logging

from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Course, Student, Assignment, Report
from .forms import UploadReportForm
from .blackboard import BlackBoard
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
        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        reports = Report.objects.filter(assignment=assignment)
        all_students = set(Student.objects.filter(courses=assignment.course))

        students_with_reports = {u.student for u in reports}
        students_without_reports = all_students - students_with_reports

        context = super(ReportView, self).get_context_data(**kwargs)
        context['students_with_reports'] = students_with_reports
        context['students_without_reports'] = students_without_reports
        return context


def upload_report_view(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)

    if request.method == 'POST':
        form = UploadReportForm(request.POST, request.FILES)
        files = request.FILES.getlist('reports')
        if form.is_valid():
            added, updated, unknown = [], [], []
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


def refresh_student_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    url = course.account.url
    username = course.account.user
    unsafe_password = course.account.unsafe_password
    bb = BlackBoard(url, username, unsafe_password)
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

        if course in s.courses.all():
            student['status'] += '- already registered'
        else:
            s.courses.add(course)
            s.save()
            student['status'] += '- now registered'

    return render(request, 'grading/refresh_student_list.html',
                  {'course': course, 'students': students})
