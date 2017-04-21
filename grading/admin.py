from django.contrib import admin

from .models import Account, Course, Student, Assignment, Report, Skills, Enrollment


@admin.register(Enrollment)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['student', 'is_active', 'final_mark', 'course']
    list_editable = ['is_active']
    list_filter = ['is_active', 'course__title']


admin.site.register(Account)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Skills)
admin.site.register(Report)
