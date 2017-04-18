from django.contrib import admin

from .models import Account, Course, Student, Assignment, Report, Skills, Enrollment

admin.site.register(Account)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Report)
admin.site.register(Skills)
admin.site.register(Enrollment)
