from core.api import fetch

from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods, require_safe

from core.api.exceptions import APIException
from core.api.resources import Profile, Report, ReportList, Site, response_list_to_dict
from core.views import build_pagination_links, require_authentication, respond_with_error, respond_with_pagination_error


def _can_moderate_reports(user):
    permissions = getattr(getattr(user, 'meta', None), 'permissions', None)
    return bool(permissions and (permissions.siteOwner or permissions.owner or permissions.moderator))


@require_authentication
@require_safe
@cache_control(must_revalidate=True, max_age=0)
def list(request):
    try:
        offset = int(request.GET.get('offset', 0))
        offset = max(0, offset // settings.PAGE_SIZE * settings.PAGE_SIZE)
    except (TypeError, ValueError):
        offset = 0

    reports_url, params, headers = ReportList.build_request(
        request.get_host(), offset=offset, access_token=request.access_token)
    request.view_requests.append(fetch.get(reports_url, params=params, headers=headers))

    try:
        responses = response_list_to_dict(fetch.map(request.view_requests))
    except APIException as exc:
        return respond_with_pagination_error(request, exc)

    user = Profile(responses[request.whoami_url], summary=False)
    if not _can_moderate_reports(user):
        return respond_with_error(request, APIException('Forbidden', 403))

    report_list = ReportList(responses[reports_url])
    view_data = {
        'user': user,
        'site': Site(responses[request.site_url]),
        'content': report_list,
        'pagination': build_pagination_links(responses[reports_url]['reports']['links'], report_list.reports),
        'site_section': 'reports',
    }
    return render(request, 'reports.html', view_data)


@require_authentication
@require_safe
@cache_control(no_cache=True, no_store=True, must_revalidate=True, max_age=0)
def pending_count(request):
    """Return the number of open cases for the admin navbar indicator."""
    try:
        count = ReportList.open_count(request.get_host(), request.access_token)
    except APIException:
        count = 0
    return JsonResponse({'count': count})


@require_authentication
@require_http_methods(['POST'])
@cache_control(must_revalidate=True, max_age=0)
def respond(request, report_id):
    try:
        responses = response_list_to_dict(fetch.map(request.view_requests))
    except APIException as exc:
        return respond_with_error(request, exc)

    user = Profile(responses[request.whoami_url], summary=False)
    if not _can_moderate_reports(user):
        return respond_with_error(request, APIException('Forbidden', 403))

    state = request.POST.get('state', '')
    if state not in ('open', 'reviewing', 'closed'):
        return HttpResponseRedirect(reverse('list-reports'))

    try:
        Report.update_state(
            request.get_host(), report_id, state, request.POST.get('note', '').strip(), request.access_token)
    except APIException as exc:
        return respond_with_error(request, exc)

    return HttpResponseRedirect(reverse('list-reports'))
