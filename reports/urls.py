from django.urls import re_path

from reports import views


urlpatterns = [
    re_path(r'^reports/types/$', views.types, name='report-types'),
    re_path(r'^reports/submit/$', views.submit, name='submit-report'),
    re_path(r'^reports/pending-count/$', views.pending_count, name='pending-report-count'),
    re_path(r'^reports/$', views.list, name='list-reports'),
    re_path(r'^reports/(?P<report_id>\d+)/respond/$', views.respond, name='respond-report'),
]
