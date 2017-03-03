from django.shortcuts import render
from django.views import generic

from .models import Course, Account


class IndexView(generic.ListView):
    model = Course
    template_name = 'grading/index.html'

class CourseView(generic.DetailView):
    model = Course
    template_name = 'grading/course.html'
