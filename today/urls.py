from django.urls import re_path

from today import views

urlpatterns = [
    re_path(r'^today/$', views.single, name='single-today'),
]
