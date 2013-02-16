#!/usr/bin/env python
# encoding: utf-8

from django.db import models


class CountVisit(models.Model):

    visits = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


""" Signals
"""
from shortener.signals import link_followed

def on_request(sender, request, **kwargs):
    sender.visits = F('visits')+1
    sender.save()

link_followed.connect(on_request)