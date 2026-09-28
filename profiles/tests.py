"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import copy
import json
import os
from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import SimpleTestCase

from core.api.resources import Profile
from core.api.resources import Site


TEST_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SimpleTest(SimpleTestCase):
    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)


class ProfileTemplateTests(SimpleTestCase):

    def setUp(self):
        with open(os.path.join(TEST_ROOT, 'core', 'tests', 'data', 'profile.json')) as profile_file:
            self.profile_data = json.load(profile_file)['data']
        with open(os.path.join(TEST_ROOT, 'core', 'tests', 'data', 'site.json')) as site_file:
            self.site = Site(json.load(site_file)['data'])

    def render_profile(self, profile_data):
        profile = Profile(profile_data, summary=False)
        profile.breadcrumb = None
        profile.email = None
        profile.isConfidential = None
        profile.is_member = False
        profile.member = False
        profile.profile_comment = None
        profile.query = SimpleNamespace(q='')
        profile.meta.links = {'self': {'href': '/profiles/5/', 'title': 'Frodo'}}

        self.site.auth0_client_id = None
        self.site.auth0_domain = None
        self.site.favicon_url = None

        search = SimpleNamespace(results=SimpleNamespace(items=[]))
        return render_to_string('profile.html', {
            'content': profile,
            'csrf_token': '',
            'item_type': 'profile',
            'search': search,
            'site': self.site,
            'site_section': 'people',
            'skipparents': False,
            'user': profile,
            'STATIC_URL': '/static/',
        })

    def test_year_one_profile_dates_do_not_break_template_rendering(self):
        profile_data = copy.deepcopy(self.profile_data)
        profile_data['created'] = '0001-01-01T00:00:00Z'
        profile_data['lastActive'] = '0001-01-01T00:00:00Z'

        rendered = self.render_profile(profile_data)

        self.assertNotIn('Member since', rendered)
        self.assertNotIn('Last active', rendered)

    def test_normal_profile_dates_are_still_rendered(self):
        rendered = self.render_profile(self.profile_data)

        self.assertIn('Member since Jan 2014', rendered)
        self.assertIn('Last active Jan 2014', rendered)
