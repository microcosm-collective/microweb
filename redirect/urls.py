from django.conf.urls import url

from redirect import views

urlpatterns = [
    url(r'.+/$', views.redirect_or_404),
]
