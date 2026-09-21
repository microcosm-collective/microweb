from django.urls import re_path

from profiles import views

urlpatterns = [
    re_path(r'^profiles/$', views.list, name='list-profiles'),
    re_path(r'^profiles/(?P<profile_id>\d+)/$', views.single, name='single-profile'),
    re_path(r'^profiles/(?P<profile_id>\d+)/edit/$', views.edit, name='edit-profile'),
    re_path(r'^profiles/(?P<profile_id>\d+)/patch/$', views.patch, name='patch-profile'),
    re_path(r'^profiles/read/$', views.mark_read, name='mark-read'),
]
