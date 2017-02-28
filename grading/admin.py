from django.contrib import admin

from .models import Account, Course, Student

admin.site.register(Account)
admin.site.register(Course)
admin.site.register(Student)
