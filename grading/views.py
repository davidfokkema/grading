from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .models import Course, Student, Assignment
from .forms import UploadReportForm
from .blackboard import BlackBoard


class IndexView(generic.ListView):
    model = Course
    template_name = 'grading/index.html'


class CourseView(generic.DetailView):
    model = Course
    template_name = 'grading/course.html'


class ReportView(generic.DetailView):
    model = Assignment
    template_name = 'grading/report.html'


class UploadReportView(generic.edit.FormView):
    template_name = 'grading/upload_reports.html'
    form_class = UploadReportForm

    def get_context_data(self, **kwargs):
        context = super(UploadReportView, self).get_context_data(**kwargs)
        context['assignment'] = Assignment.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('reports')
        if form.is_valid():
            for f in files:
                print(f.name)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # provide a valid success_url, JIT-style because we need to have
        # self.kwargs defined
        self.success_url = reverse('report_assignment',
                                   kwargs={'pk': self.kwargs['pk']})
        return super(UploadReportView, self).form_valid(form)


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


# def upload_report(request, assignment_id):
#     assignment = Assignment.objects.get(pk=assignment_id)
#
#     if request.method == 'POST':
#         form = UploadReportForm(request.POST, request.FILES))
#         if form.is_valid():
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadReportForm()
#     return render(request, 'grading/report_assignment.html',
#                   {'assignment': assignment, 'form': form})
