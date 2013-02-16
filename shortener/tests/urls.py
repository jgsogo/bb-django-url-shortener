#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, include, url


from shortener.views import follow
urlpatterns = patterns('',
    url(r'^(?P<base62>\w+)$', follow, name='short_link'),
)