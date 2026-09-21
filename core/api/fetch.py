import logging
from concurrent.futures import ThreadPoolExecutor

import requests
from django.conf import settings

logger = logging.getLogger('core.api.fetch')

DEFAULT_TIMEOUT = getattr(settings, 'API_TIMEOUT', 30)

# One executor per process, shared by all Django requests. Sized for the
# number of concurrently-served requests (gunicorn --threads) multiplied by
# the largest view batch (~6 API calls), with headroom. Tasks never submit
# subtasks, so saturation queues rather than deadlocks.
_executor = ThreadPoolExecutor(
    max_workers=getattr(settings, 'API_EXECUTOR_MAX_WORKERS', 64),
    thread_name_prefix='api-fetch',
)


class APIRequest(object):
    """Deferred GET descriptor. Replaces grequests.AsyncRequest: holds the
    request details without performing any I/O until passed to map()."""

    __slots__ = ('url', 'params', 'headers')

    def __init__(self, url, params=None, headers=None):
        self.url = url
        self.params = params
        self.headers = headers


def get(url, params=None, headers=None):
    return APIRequest(url, params=params, headers=headers)


def _send(api_request):
    try:
        # requests follows redirects by default; response.history[0].url keeps
        # the originally-requested URL, which response_list_to_dict keys on.
        return requests.get(
            api_request.url,
            params=api_request.params,
            headers=api_request.headers,
            timeout=DEFAULT_TIMEOUT,
        )
    except requests.RequestException as e:
        # Preserve the grequests.map contract: a failed request maps to None.
        logger.error('API request failed: %s: %s' % (api_request.url, str(e)))
        return None


def map(api_requests):
    """Execute a batch of APIRequests concurrently, returning responses in
    the same order. Failed requests yield None entries."""
    if not api_requests:
        return []
    if len(api_requests) == 1:
        return [_send(api_requests[0])]
    return list(_executor.map(_send, api_requests))
