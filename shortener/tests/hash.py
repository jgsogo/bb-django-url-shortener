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
@override_settings(SHORTENER_MIN_HASH_LENGTH=1)
@override_settings(SHORTENER_MAX_HASH_LENGTH=2)
class HashTest(TestCase):

    class LinkProxyModel(object):
        def __init__(self, id):
            self.id = id
        def save(self):
            pass

    def test_length(self):
        max_possibilities = int(pow(len(Link.baseconverter.digits), settings.SHORTENER_MAX_HASH_LENGTH)) # TODO: how to apply modified settings to test? int(Link.max_shortened_available())
        log.debug("Testing uniqueness for %s possibilities" % max_possibilities)
        instance = HashTest.LinkProxyModel(0)
        for i in xrange(max_possibilities-1):
            hash = Link.generate_unique_hash(instance, settings.SHORTENER_MIN_HASH_LENGTH, settings.SHORTENER_MAX_HASH_LENGTH)
            instance.id += 1
        self.assertEqual(settings.SHORTENER_MAX_HASH_LENGTH, len(hash))
        # Next one will have one more char (model raises exception)
        hash = Link.generate_unique_hash(instance, settings.SHORTENER_MIN_HASH_LENGTH, settings.SHORTENER_MAX_HASH_LENGTH)
        self.assertNotEqual(settings.SHORTENER_MAX_HASH_LENGTH, len(hash))

    @override_settings(SHORTENER_HASH_STRATEGY=generate_unique_random_hash)
    def test_random(self):
        max_possibilities = int(pow(len(Link.baseconverter.digits), settings.SHORTENER_MAX_HASH_LENGTH)) # TODO: how to apply modified settings to test? int(Link.max_shortened_available())
        log.debug("Testing uniqueness for %s possibilities" % max_possibilities)
        instance = HashTest.LinkProxyModel(0)
        for i in xrange(max_possibilities-1):
            hash = Link.generate_unique_hash(instance, settings.SHORTENER_MIN_HASH_LENGTH, settings.SHORTENER_MAX_HASH_LENGTH)
        self.assertEqual(settings.SHORTENER_MAX_HASH_LENGTH, len(hash))
        # Next one will have one more char.
        hash = Link.generate_unique_hash(instance, settings.SHORTENER_MIN_HASH_LENGTH, settings.SHORTENER_MAX_HASH_LENGTH)
        self.assertNotEqual(settings.SHORTENER_MAX_HASH_LENGTH, len(hash))
