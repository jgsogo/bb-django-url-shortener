#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, include, url
from chimp_shortener_data.views import robots


urlpatterns = patterns('',
    url(r'^robots\.txt$', robots, name='robots'),
    )
