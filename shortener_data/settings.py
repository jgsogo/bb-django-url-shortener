#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings

ROBOTS_FILEPATH = getattr(settings, 'SHORTENER_ROBOTS_STR', None)