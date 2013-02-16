#!/usr/bin/env python
# encoding: utf-8

import logging

from math import pow
from django.test import TestCase
from django.test.utils import override_settings
from django.conf import settings

from shortener.models import Link
from shortener.utils.hash_random import generate_unique_random_hash

log = logging.getLogger(__name__)

@override_settings(SHORTENER_LINK_UNIQUENESS=True)
@override_settings(SHORTENER_MAX_HASH_LENGTH=2)
class HashTest(TestCase):

    def test_length(self):
        max_possibilities = int(pow(len(Link.baseconverter.digits), settings.SHORTENER_MAX_HASH_LENGTH))
        log.debug("Testing uniqueness for %s possibilities" % max_possibilities)
        for i in xrange(max_possibilities-1):
            obj = Link.create('http://this.isvalid.url')
        self.assertEqual(settings.SHORTENER_MAX_HASH_LENGTH, len(obj._hash))
        # Next one will have one more char (model raises exception)
        obj = Link.create('http://this.isvalid.url')
        self.assertNotEqual(settings.SHORTENER_MAX_HASH_LENGTH, len(obj._hash))

    @override_settings(SHORTENER_HASH_STRATEGY=generate_unique_random_hash)
    def test_random(self):
        max_possibilities = int(pow(len(Link.baseconverter.digits), settings.SHORTENER_MAX_HASH_LENGTH))
        log.debug("Testing uniqueness for %s possibilities" % max_possibilities)
        for i in xrange(max_possibilities-1):
            obj = Link.create('http://this.isvalid.url')
        self.assertEqual(settings.SHORTENER_MAX_HASH_LENGTH, len(obj._hash))
        # Next one will have one more char.
        obj = Link.create('http://this.isvalid.url')
        self.assertNotEqual(settings.SHORTENER_MAX_HASH_LENGTH, len(obj._hash))
