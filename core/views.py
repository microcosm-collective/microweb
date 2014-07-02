import requests
from requests import RequestException

import grequests
import datetime
import logging

from functools import wraps

from django.conf import settings

from django.core.exceptions import ValidationError

from django.http import HttpResponseNotFound
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import redirect
from django.shortcuts import render

from django.template import RequestContext
from django.template import loader

from django.views.decorators.http import require_http_methods

from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView

from core.api.exceptions import APIException
from core.api.resources import FileMetadata
from core.api.resources import Comment
from core.api.resources import Profile
from core.api.resources import WhoAmI
from core.api.resources import Attachment
from core.api.resources import response_list_to_dict
from core.api.resources import Site
from core.api.resources import Legal

from core.api.resources import build_url

logger = logging.getLogger('core.views')

def exception_handler(view_func):
    """
    Decorator for view functions that raises appropriate
    errors to the user and passes data to the error view.

    Forbidden and Not Found are the only statuses that are
    communicated to the visitor. All other errors should
    be handled in client code or a generic error page will
    be displayed.
    """

    @wraps(view_func)
    def decorator(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except APIException as e:
            if e.status_code == 401 or e.status_code == 403:
                return ErrorView.forbidden(request)
            elif e.status_code == 404:
                return ErrorView.not_found(request)
            elif e.status_code == 400:
                # Error code 14 indicates that the requested forum does not exist.
                if e.detail['errorCode'] == 14:
                    return HttpResponseRedirect('http://microco.sm')
            else:
                raise
    return decorator

def respond_with_error(request, exception):

    if not isinstance(exception, APIException):
        logger.error(str(exception))
        return ErrorView.server_error(request)

    if exception.status_code == 404:
        return ErrorView.not_found(request)
    elif exception.status_code == 403:
        return ErrorView.forbidden(request)
    else:
        return ErrorView.server_error(request)

def require_authentication(view_func):
    """
    Returns HTTP 401 if request.access_token is not present.
    """

    @wraps(view_func)
    def decorator(request, *args, **kwargs):
        if hasattr(request, 'access_token'):
            return view_func(request, *args, **kwargs)
        else:
            return ErrorView.forbidden(request)
    return decorator

def build_pagination_links(request, paged_list):
    """
    This takes the data sent in the 'links' part of an api response
    and generates a dictionary of navigation links based on that.
    """

    if not hasattr(paged_list, 'page'):
        return {}

    page_nav = {
    'page': int(paged_list.page),
    'total_pages': int(paged_list.total_pages),
    'limit': int(paged_list.limit),
    'offset': int(paged_list.offset)
    }

    for item in request:
        item['href'] = str.replace(str(item['href']), '/api/v1', '')
        page_nav[item['rel']] = item

    return page_nav

def process_attachments(request, comment):

    """
    For the provided request, check if files are to be attached or deleted
    from the provided comment. Raises a ValidationError if any files are larger
    than 5MB.
    """

    # Check if any existing comment attachments are to be deleted.
    if request.POST.get('attachments-delete'):
        attachments_delete = request.POST.get('attachments-delete').split(",")
        for fileHash in attachments_delete:
            Attachment.delete(request.get_host(), Comment.api_path_fragment, comment.id, fileHash)

    # Check if any files have been uploaded with the request.
    if request.FILES.has_key('attachments'):
        for f in request.FILES.getlist('attachments'):
            file_request = FileMetadata.from_create_form(f)
            # Maximum file size is 5MB.
            if len(file_request.file[f.name]) >= 5242880:
                raise ValidationError
            # Associate attachment with comment using attachments API.
            else:
                file_metadata = file_request.create(request.get_host(), request.access_token)
                Attachment.create(request.get_host(), file_metadata.file_hash,
                                  comment_id=comment.id, access_token=request.access_token, file_name=f.name)


class LegalView(object):
    list_template = 'legals.html'
    single_template = 'legal.html'

    @staticmethod
    @require_http_methods(['GET',])
    def list(request):
        try:
            responses = response_list_to_dict(grequests.map(request.view_requests))
        except APIException as exc:
            return respond_with_error(request, exc)

        view_data = {
            'site': Site(responses[request.site_url]),
            'user': Profile(responses[request.whoami_url], summary=False) if request.whoami_url else None,
            'site_section': 'legal'
        }
        return render(request, LegalView.list_template, view_data)

    @staticmethod
    @require_http_methods(['GET',])
    def single(request, doc_name):
        if not doc_name in ['cookies', 'privacy', 'terms']:
            return HttpResponseNotFound()

        url, params, headers = Legal.build_request(request.get_host(), doc=doc_name)
        request.view_requests.append(grequests.get(url, params=params, headers=headers))
        try:
            responses = response_list_to_dict(grequests.map(request.view_requests))
        except APIException as exc:
            return respond_with_error(request, exc)

        legal = Legal.from_api_response(responses[url])

        view_data = {
            'site': Site(responses[request.site_url]),
            'user': Profile(responses[request.whoami_url], summary=False) if request.whoami_url else None,
            'content': legal,
            'site_section': 'legal',
            'page_section': doc_name
        }
        return render(request, LegalView.single_template, view_data)


class ErrorView(object):
    @staticmethod
    def not_found(request):
        view_data = {}
        view_requests = []

        if request.COOKIES.has_key('access_token'):
            request.access_token = request.COOKIES['access_token']
            whoami_url, params, headers = WhoAmI.build_request(request.get_host(), request.access_token)
            view_requests.append(grequests.get(whoami_url, params=params, headers=headers))

        site_url, params, headers = Site.build_request(request.get_host())
        view_requests.append(grequests.get(request.site_url, params=params, headers=headers))

        responses = response_list_to_dict(grequests.map(request.view_requests))
        view_data['user'] = Profile(responses[whoami_url], summary=False)
        view_data['site'] = Site(responses[site_url])

        context = RequestContext(request, view_data)
        return HttpResponseNotFound(loader.get_template('404.html').render(context))

    @staticmethod
    def forbidden(request):
        view_data = {}
        view_requests = []

        if request.COOKIES.has_key('access_token'):
            request.access_token = request.COOKIES['access_token']
            whoami_url, params, headers = WhoAmI.build_request(request.get_host(), request.access_token)
            view_requests.append(grequests.get(whoami_url, params=params, headers=headers))

        site_url, params, headers = Site.build_request(request.get_host())
        view_requests.append(grequests.get(request.site_url, params=params, headers=headers))

        responses = response_list_to_dict(grequests.map(request.view_requests))
        view_data['user'] = Profile(responses[whoami_url], summary=False)
        view_data['site'] = Site(responses[site_url])

        context = RequestContext(request, view_data)
        return HttpResponseForbidden(loader.get_template('403.html').render(context))

    @staticmethod
    def server_error(request):
        view_data = {}
        view_requests = []

        if request.COOKIES.has_key('access_token'):
            request.access_token = request.COOKIES['access_token']
            whoami_url, params, headers = WhoAmI.build_request(request.get_host(), request.access_token)
            view_requests.append(grequests.get(whoami_url, params=params, headers=headers))

        site_url, params, headers = Site.build_request(request.get_host())
        view_requests.append(grequests.get(request.site_url, params=params, headers=headers))

        responses = response_list_to_dict(grequests.map(request.view_requests))
        view_data['user'] = Profile(responses[whoami_url], summary=False)
        view_data['site'] = Site(responses[site_url])

        context = RequestContext(request, view_data)
        return HttpResponseServerError(loader.get_template('500.html').render(context))


class AuthenticationView(object):

    @staticmethod
    def login(request):
        """
        Log a user in. Creates an access_token using a persona
        assertion and the client secret. Sets this access token as a cookie.
        'target_url' based as a GET parameter determines where the user is
        redirected.
        """

        target_url = request.POST.get('target_url')
        assertion = request.POST.get('Assertion')
        postdata = {
            'Assertion': assertion,
            'ClientSecret':settings.CLIENT_SECRET
        }

        url = build_url(request.get_host(), ['auth'])
        try:
            response = requests.post(url, data=postdata, headers={})
        except RequestException:
            return ErrorView.server_error(request)
        access_token = response.json()['data']

        response = HttpResponseRedirect(target_url if target_url != '' else '/')
        expires = datetime.datetime.fromtimestamp(2 ** 31 - 1)
        response.set_cookie('access_token', access_token, expires=expires, httponly=True)
        return response

    @staticmethod
    @require_http_methods(["POST"])
    def logout(request):
        """
        Log a user out. Issues a DELETE request to the backend for the
        user's access_token, and issues a delete cookie header in response to
        clear the user's access_token cookie.
        """

        response = redirect('/')
        if request.COOKIES.has_key('access_token'):
            response.delete_cookie('access_token')
            url = build_url(request.get_host(), ['auth', request.access_token])
            try:
                requests.post(url, params={'method': 'DELETE', 'access_token': request.access_token})
            except RequestException:
                return ErrorView.server_error(request)

        return response


def echo_headers(request):
    view_data = '<html><body><table>'
    for key in request.META.keys():
        view_data += '<tr><td>%s</td><td>%s</td></tr>' % (key, request.META[key])
    view_data += '</table></body></html>'
    return HttpResponse(view_data, content_type='text/html')


class FaviconView(RedirectView):
    def get_redirect_url(self, **kwargs):
        return settings.STATIC_URL + 'img/favico.png'


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'

    def get_context_data(self, **kwargs):
        return super(RobotsView, self).get_context_data(**kwargs)
