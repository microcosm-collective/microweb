"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase


class SimpleTest(SimpleTestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class CommentTemplateTests(SimpleTestCase):
    def test_single_comment_without_author_profile_id_does_not_raise(self):
        """
        The API may omit or redact the author ID when the author is not
        visible on the current site. Rendering that comment must not turn a
        valid response into a 500 through a failed profile URL reversal.
        """
        permissions = SimpleNamespace(siteOwner=False, update=False, delete=False)
        meta = SimpleNamespace(
            links={
                'up': {'href': '/conversations/1/', 'title': 'Conversation'},
                'commentPage': {'href': '/conversations/1/'},
            },
            permissions=permissions,
            created_by=SimpleNamespace(profile_name='hidden author'),
        )
        content = SimpleNamespace(
            id=123,
            html='Comment body',
            query={},
            title='',
            description='',
            meta=meta,
        )
        site = SimpleNamespace(
            subdomain_key='example',
            theme_id=1,
            link_color='',
            background_color='',
            logo_url='',
            favicon_url='',
            background_url='',
            background_position='',
            title='Example',
            description='',
            menu=[],
            auth0_domain='',
            auth0_client_id='',
        )

        rendered = render_to_string(
            'comment.html',
            {
                'content': content,
                'site': site,
                'user': None,
                'attachments': {},
                'site_section': '',
                'STATIC_URL': '/static/',
            },
            request=RequestFactory().get('/'),
        )

        self.assertIn('Comment body', rendered)
        self.assertIn('Click here to read the full conversation.', rendered)
        self.assertNotIn("href=\"/profiles/\"", rendered)
