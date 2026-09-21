from django.urls import re_path

from redirect import views

urlpatterns = [
    re_path(r'.+/$', views.redirect_or_404),
]
