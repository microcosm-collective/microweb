from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core.views import ErrorView

from microweb import settings

# In the following, redirect.urls *MUST* remain the very last URL as it handles
# all urls as potentially being a 404
urlpatterns = [
    "",
    url(r"", include("microcosms.urls")),
    url(r"", include("core.urls")),
    url(r"", include("conversations.urls")),
    url(r"", include("events.urls")),
    url(r"", include("huddles.urls")),
    url(r"", include("mwcomments.urls")),
    url(r"", include("profiles.urls")),
    url(r"", include("updates.urls")),
    url(r"", include("search.urls")),
    url(r"", include("today.urls")),
    url(r"", include("trending.urls")),
    url(r"", include("moderation.urls")),
    url(r"", include("ignored.urls")),
    url(r"", include("redirect.urls")),
]

# Serve static files with gunicorn if DEBUG is true.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

handler403 = ErrorView.forbidden
handler404 = ErrorView.not_found
handler500 = ErrorView.server_error
