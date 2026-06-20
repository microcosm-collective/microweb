import logging

from django.core.cache import cache
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect

from core.api.resources import Site
from core.api.exceptions import APIException

from requests import RequestException

logger = logging.getLogger('core.middleware.redirect')


class DomainRedirectMiddleware:
    """
    Where a site has a custom domain, the user should be permanently redirected to
    the custom domain from the microcosm subdomain.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response is not None:
            return response
        return self.get_response(request)

    def process_request(self, request):

        host = request.get_host()

        # Only look at requests to example.microcosm.app
        if host.endswith(settings.API_DOMAIN_NAME):

            # Fetch site from cache
            try:
                site = cache.get(host)
            except Exception as e:
                logger.error('Memcached GET error: %s' % str(e))
                site = None

            # Not in cache or retrieval failed
            if site is None:
                try:
                    site = Site.retrieve(host)
                    try:
                        cache.set(host, site, timeout=300)
                    except Exception as e:
                        logger.error('Memcached SET error: %s' % str(e))
                except APIException as e:
                    # HTTP 400 indicates a non-existent site.
                    if e.status_code == 404:
                        return HttpResponseRedirect('http://microcosm.app')
                    logger.error('APIException: %s' % str(e))
                    return HttpResponseRedirect(reverse('server-error'))
                except RequestException as e:
                    logger.error('RequestException: %s' % str(e))
                    return HttpResponseRedirect(reverse('server-error'))

            # Forum owner has configured their own domain, so 301 the client.
            if hasattr(site, 'domain') and site.domain:
                # We don't support SSL on custom domains yet, so ensure the scheme is http.
                location = 'http://' + site.domain + request.get_full_path()
                logger.debug('Redirecting subdomain to: %s' % location)
                return HttpResponsePermanentRedirect(location)

        return None
