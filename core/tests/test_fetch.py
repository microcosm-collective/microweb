import unittest
from unittest.mock import Mock, patch

import requests

from core.api import fetch
from core.api.resources import response_list_to_dict


def fake_response(url, data, history=None):
    response = Mock()
    response.url = url
    response.history = history or []
    response.json.return_value = {'error': '', 'data': data}
    response.status_code = 200
    return response


class FetchTests(unittest.TestCase):

    @patch('requests.get')
    def test_map_preserves_order(self, mock_get):
        mock_get.side_effect = lambda url, **kwargs: fake_response(url, url)
        batch = [
            fetch.get('http://example.org/api/v1/site', params={'a': 1}, headers={'h': '1'}),
            fetch.get('http://example.org/api/v1/whoami'),
            fetch.get('http://example.org/api/v1/conversations/1'),
        ]
        responses = fetch.map(batch)
        self.assertEqual(
            [r.url for r in responses],
            [b.url for b in batch],
        )
        mock_get.assert_any_call(
            'http://example.org/api/v1/site',
            params={'a': 1},
            headers={'h': '1'},
            timeout=fetch.DEFAULT_TIMEOUT,
        )

    @patch('requests.get')
    def test_failed_request_maps_to_none(self, mock_get):
        def side_effect(url, **kwargs):
            if 'bad' in url:
                raise requests.RequestException('boom')
            return fake_response(url, url)
        mock_get.side_effect = side_effect
        responses = fetch.map([
            fetch.get('http://example.org/good'),
            fetch.get('http://example.org/bad'),
        ])
        self.assertIsNotNone(responses[0])
        self.assertIsNone(responses[1])

    def test_map_empty_batch(self):
        self.assertEqual(fetch.map([]), [])

    def test_response_list_to_dict_keys_redirect_by_original_url(self):
        # The /whoami case: the API 302s to /profiles/{id}; the response must
        # be keyed by the originally-requested whoami URL.
        whoami_url = 'http://example.org/api/v1/whoami'
        response = fake_response(
            'http://example.org/api/v1/profiles/1',
            {'id': 1},
            history=[Mock(url=whoami_url)],
        )
        site_url = 'http://example.org/api/v1/site'
        site_response = fake_response(site_url, {'title': 'a site'})

        # None entries (failed requests) must be skipped.
        responses = response_list_to_dict([response, site_response, None])
        self.assertEqual(responses[whoami_url], {'id': 1})
        self.assertEqual(responses[site_url], {'title': 'a site'})
