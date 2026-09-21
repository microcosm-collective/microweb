from django.urls import re_path

from trending import views


urlpatterns = [
    re_path(r'^trending/$', views.list, name='list-trending'),
]
