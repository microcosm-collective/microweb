from django.urls import re_path

from huddles import views


urlpatterns = [
    # Huddles
    re_path(r'^huddles/$', views.list, name='list-huddle'),
    re_path(r'^huddles/create/$', views.create, name='create-huddle'),
    re_path(r'^huddles/(?P<huddle_id>\d+)/$' , views.single, name='single-huddle'),
    re_path(r'^huddles/(?P<huddle_id>\d+)/leave/$', views.delete, name='delete-huddle'),
    re_path(r'^huddles/(?P<huddle_id>\d+)/invite/$', views.invite, name='invite-huddle'),
    re_path(r'^huddles/(?P<huddle_id>\d+)/newest/$', views.newest, name='newest-huddle'),
]