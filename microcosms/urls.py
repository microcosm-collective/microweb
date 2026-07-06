from django.urls import re_path

from microcosms import views


urlpatterns = [
    re_path(r'^$', views.root_microcosm, name='index'),
    re_path(r'^microcosms/$', views.root_microcosm, name='list-microcosms'),
    re_path(r'^microcosms/create/$', views.create_microcosm, name='create-microcosm'),
    re_path(r'^microcosms/(?P<microcosm_id>\d+)/$', views.single_microcosm, name='single-microcosm'),
    re_path(r'^microcosms/(?P<parent_id>\d+)/create/microcosm/$', views.create_microcosm, name='create-child-microcosm'),
    re_path(r'^microcosms/(?P<microcosm_id>\d+)/edit/$', views.edit_microcosm, name='edit-microcosm'),
    re_path(r'^microcosms/(?P<microcosm_id>\d+)/delete/$', views.delete_microcosm, name='delete-microcosm'),

    re_path(r'^microcosms/(?P<microcosm_id>\d+)/memberships/$', views.list_members, name="list-memberships"),
    re_path(r'^microcosms/(?P<microcosm_id>\d+)/memberships/create/$', views.create_members,
        name="create-memberships"),
    re_path(r'^microcosms/(?P<microcosm_id>\d+)/memberships/(?P<group_id>\d+)/edit/$', views.edit_members,
        name="edit-memberships"),

    # Proxy and batch requests to the backend
    re_path(r'^microcosms/(?P<microcosm_id>\d+)/memberships/api/$', views.members_api, name="api-memberships"),
]