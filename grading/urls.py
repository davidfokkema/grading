from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.CourseView.as_view(), name='course'),
    url(r'^(?P<course_id>[0-9]+)/refresh/students/$',
        views.refresh_student_list, name='refresh_students'),
    # url(r'^upload/reports/(?P<assignment_id>[0-9]+)/$',
    #     views.upload_report, name='upload_reports')
    url(r'^upload/reports/(?P<pk>[0-9]+)/$',
        views.UploadReportView.as_view(), name='upload_reports')
]
