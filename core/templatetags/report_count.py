from django import template

from core.api.exceptions import APIException
from core.api.resources import ReportList


register = template.Library()


@register.simple_tag
def report_count(user, request):
    permissions = getattr(getattr(user, 'meta', None), 'permissions', None)
    if not permissions or not (
        permissions.siteOwner or permissions.moderator
    ):
        return 0

    try:
        return ReportList.open_count(request.get_host(), request.access_token)
    except APIException:
        return 0
