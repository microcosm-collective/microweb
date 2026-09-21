from django.urls import re_path

from events import views

urlpatterns = [
    # Events
    re_path(r'^microcosms/(?P<microcosm_id>\d+)/create/event/$', views.create, name='create-event'),
    re_path(r'^events/(?P<event_id>\d+)/$', views.single, name='single-event'),
    re_path(r'^events/(?P<event_id>\d+)/csv/$', views.csv, name='csv-event'),
    re_path(r'^events/(?P<event_id>\d+)/edit/$', views.edit, name='edit-event'),
    re_path(r'^events/(?P<event_id>\d+)/delete/$', views.delete, name='delete-event'),
    re_path(r'^events/(?P<event_id>\d+)/newest/$', views.newest, name='newest-event'),
    # RSVP to an event
    re_path(r'^events/(?P<event_id>\d+)/rsvp/$', views.rsvp, name='rsvp-event'),

    # Proxy geocoding requests to the backend
    re_path(r'^geocode/$', views.geocode, name='geocode'),
]