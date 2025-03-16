from django.conf.urls import url

from profiles import views

urlpatterns = [
    url(r'^profiles/$', views.list, name='list-profiles'),
    url(r'^profiles/(?P<profile_id>\d+)/$', views.single, name='single-profile'),
    url(r'^profiles/(?P<profile_id>\d+)/edit/$', views.edit, name='edit-profile'),
    url(r'^profiles/(?P<profile_id>\d+)/patch/$', views.patch, name='patch-profile'),
    url(r'^profiles/read/$', views.mark_read, name='mark-read'),
]
