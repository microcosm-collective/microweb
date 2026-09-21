from django.urls import re_path

from search import views


urlpatterns = [
    re_path(r'^search/$', views.single, name='single-search'),
]
