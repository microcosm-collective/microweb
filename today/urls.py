from django.conf.urls import url

from today import views

urlpatterns = ['',
     url(r'^today/$', views.single, name='single-today'),
]
