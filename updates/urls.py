from django.urls import re_path

from updates.views import UpdateView
from updates.views import WatcherView
from updates.views import UpdatePreferenceView


urlpatterns = [
    # Updates
    re_path(r'^updates/$', UpdateView.list, name='list-updates'),
    re_path(r'^updates/settings/$', UpdatePreferenceView.settings, name='updates-settings'),

    # Watchers
    re_path(r'^watchers/$', WatcherView.single, name='single-watcher'),
]
