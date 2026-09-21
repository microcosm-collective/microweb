from django.urls import re_path

from conversations import views

urlpatterns = [
    re_path(r'^microcosms/(?P<microcosm_id>\d+)/create/conversation/$', views.create, name='create-conversation'),
    re_path(r'^conversations/(?P<conversation_id>\d+)/$' , views.single, name='single-conversation'),
    re_path(r'^conversations/(?P<conversation_id>\d+)/edit/$', views.edit, name='edit-conversation'),
    re_path(r'^conversations/(?P<conversation_id>\d+)/delete/$', views.delete, name='delete-conversation'),
    re_path(r'^conversations/(?P<conversation_id>\d+)/newest/$', views.newest, name='newest-conversation'),
]
