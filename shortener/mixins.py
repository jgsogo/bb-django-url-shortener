#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User

from shortener.settings import LOGIN_REQUIRED


class EnhancedLink(models.Model):

    user = models.ForeignKey(User, blank=not LOGIN_REQUIRED, null= not LOGIN_REQUIRED)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def create(cls, url, user):
        instance = super(EnhancedLink, cls).create(url, commit=False)
        instance.user = user
        instance.save()
        return instance