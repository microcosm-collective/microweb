from django.urls import re_path

from ignored import views

urlpatterns = [
    re_path(r'^ignored/$',  views.ignored, name='list-ignored'),
     re_path(r'^ignore/$',   views.ignore,  name='ignore-item'),
     re_path(r'^unignore/$', views.ignore,  name='unignore-item'),
]
