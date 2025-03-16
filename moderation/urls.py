from django.conf.urls import url

from moderation import views


urlpatterns = ['',
    url(r'^moderate/$',    views.confirm,  name='moderate-item'),
    url(r'^moderate/do/$', views.moderate, name='actually-moderate-item'),
]
