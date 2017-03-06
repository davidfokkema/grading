from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Course, Account, Student
from .blackboard import BlackBoard


class IndexView(generic.ListView):
    model = Course
    template_name = 'grading/index.html'


class CourseView(generic.DetailView):
    model = Course
    template_name = 'grading/course.html'


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
