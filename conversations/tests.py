from django.test import SimpleTestCase

from unittest.mock import patch

from core.tests.tests import attachments_body
from core.tests.tests import fake_api_response
from core.tests.tests import load_fixture


class SingleConversationTests(SimpleTestCase):

    @patch('requests.get')
    def test_renders_comment_attachments(self, mock_get):
        conversation = load_fixture('conversation_with_paginated_comments.json')
        conversation['data']['comments']['items'][1]['attachments'] = 1
        bodies = {
            'https://dev1.microcosm.app/api/v1/site': load_fixture('site.json'),
            'https://dev1.microcosm.app/api/v1/conversations/1': conversation,
            'https://dev1.microcosm.app/api/v1/comments/2/attachments': attachments_body('diagram.png'),
        }
        mock_get.side_effect = lambda url, **kwargs: fake_api_response(url, bodies[url])

        response = self.client.get('/conversations/1/', HTTP_HOST='dev1.microcosm.app')

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<img src="https://dev1.microcosm.app/api/v1/files/2a5a2cc004aa06939fbc78630876617ce84b5359.png" '
            'alt="diagram.png" title="diagram.png" />',
            html=True,
        )
