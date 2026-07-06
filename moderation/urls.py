from django.urls import re_path

from moderation import views


urlpatterns = [
    re_path(r'^moderate/$',    views.confirm,  name='moderate-item'),
    re_path(r'^moderate/do/$', views.moderate, name='actually-moderate-item'),
]
