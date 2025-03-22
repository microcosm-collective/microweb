from django.conf.urls import url

from trending import views


urlpatterns = [
     url(r'^trending/$', views.list, name='list-trending'),
]
