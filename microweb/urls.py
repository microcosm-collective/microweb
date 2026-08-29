from django.urls import include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core.views import ErrorView

from django.conf import settings

# In the following, redirect.urls *MUST* remain the very last URL as it handles
# all urls as potentially being a 404
urlpatterns = [
    re_path(r'', include('microcosms.urls')),
    re_path(r'', include('core.urls')),
    re_path(r'', include('conversations.urls')),
    re_path(r'', include('events.urls')),
    re_path(r'', include('huddles.urls')),
    re_path(r'', include('comments.urls')),
    re_path(r'', include('profiles.urls')),
    re_path(r'', include('updates.urls')),
    re_path(r'', include('search.urls')),
    re_path(r'', include('today.urls')),
    re_path(r'', include('trending.urls')),
    re_path(r'', include('moderation.urls')),
    re_path(r'', include('ignored.urls')),
    re_path(r'', include('redirect.urls')),
]

# Serve static files with gunicorn if DEBUG is true.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

handler403 = ErrorView.forbidden
handler404 = ErrorView.not_found
handler500 = ErrorView.server_error
