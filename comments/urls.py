from django.urls import re_path

from comments import views

urlpatterns = [
    re_path(r'comments/create/$', views.create, name='create-comment'),
    re_path(r'comments/(?P<comment_id>\d+)/$', views.single, name='single-comment'),
    re_path(r'comments/(?P<comment_id>\d+)/edit/$', views.edit, name='edit-comment'),
    re_path(r'comments/(?P<comment_id>\d+)/delete/$', views.delete, name='delete-comment'),
    re_path(r'comments/(?P<comment_id>\d+)/incontext/$', views.incontext, name='incontext-comment'),
    re_path(r'comments/(?P<comment_id>\d+)/source/$', views.source, name='source-comment'),
    re_path(r'comments/(?P<comment_id>\d+)/attachments/$', views.attachments, name='attachment-comment'),
]