from unittest.mock import patch

from django.test import SimpleTestCase
from django.test import RequestFactory

from search.views import single


class SearchViewTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('search.views.fetch.map')
    def test_invalid_offset_returns_bad_request(self, fetch_map):
        for offset in (
            '%27%3E%3Casdf%20alt%3D%22%22%3E-f3f3',
            '%2527%253E%253Casdf%2520alt%253D%2522%2522%253E-f3f3',
        ):
            with self.subTest(offset=offset):
                request = self.factory.get('/search/?offset=%s' % offset)
                response = single(request)

                self.assertEqual(response.status_code, 400)
        fetch_map.assert_not_called()

    @patch('search.views.fetch.map')
    def test_negative_offset_returns_bad_request(self, fetch_map):
        request = self.factory.get('/search/?offset=-1')

        response = single(request)

        self.assertEqual(response.status_code, 400)
        fetch_map.assert_not_called()
