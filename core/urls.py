from django.urls import re_path

from core.views import AuthenticationView
from core.views import Auth0View
from core.views import ErrorView
from core.views import FaviconView
from core.views import RobotsView
from core.views import LegalView
from core.views import echo_headers


urlpatterns = [
    # Static
    re_path(r'^robots\.txt$', RobotsView.as_view()),
    re_path(r'^favicon\.ico$', FaviconView.as_view()),

    # Auth
    re_path(r'^login/$', AuthenticationView.login, name='login'),
    re_path(r'^auth0login/$', Auth0View.login, name='auth0login'),
    re_path(r'^logout/$', AuthenticationView.logout, name='logout'),

    # Legal
    re_path(r'^about/$', LegalView.list, name='list-legal'),
    re_path(r'^about/(?P<doc_name>[a-z]+)/$', LegalView.single, name='single-legal'),

    # Echoes request headers
    re_path(r'^headers/', echo_headers),

    # Break things
    re_path(r'error/', ErrorView.server_error, name='server-error'),
    re_path(r'notfound/', ErrorView.not_found),
    re_path(r'forbidden/', ErrorView.forbidden),
]
