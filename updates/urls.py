from django.conf.urls import url

from updates.views import UpdateView
from updates.views import WatcherView
from updates.views import UpdatePreferenceView


urlpatterns = [
    # Updates
    url(r"^updates/$", UpdateView.list, name="list-updates"),
    url(r"^updates/settings/$", UpdatePreferenceView.settings, name="updates-settings"),
    # Watchers
    url(r"^watchers/$", WatcherView.single, name="single-watcher"),
]
