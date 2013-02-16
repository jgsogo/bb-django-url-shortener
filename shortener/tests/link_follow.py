#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from django.test.client import Client

from shortener.models import Link


class LinkFollowTest(TestCase):
    urls = 'shortener.tests.urls'

    def setUp(self):
        self.url = 'http://this.is.valid.url/with/pattern/'
        self.link = Link.create(self.url)
        self.c = Client()

    def test_linkfollow(self):
        response = self.c.get('/%s' % self.link._hash)
        self.assertEqual(response.status_code, 302)
        response = self.c.get('/%s' % self.link._hash, follow=True)
        self.assertEqual(self.url, response.redirect_chain[0][0])

