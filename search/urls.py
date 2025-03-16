from django.conf.urls import url

from search import views


urlpatterns = ['',
   url(r'^search/$', views.single, name='single-search'),
]
