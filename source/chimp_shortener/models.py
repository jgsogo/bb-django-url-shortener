import base64
import os
import logging

from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from chimp_shortener.settings import LINK_UNIQUENESS, LINK_VALIDATION, HASH_SEED_LENGTH, SITE_BASE_URL, HASH_STRATEGY
from chimp_shortener.baseconv import base62

log = logging.getLogger(__name__)

class Link(models.Model):
    _hash = models.CharField(max_length=8) # n-char unique random string
    url = models.CharField(max_length=512) # http://www.boutell.com/newfaq/misc/urllength.html
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.url

    def get_short_link(self):
        return u'%s%s' % (SITE_BASE_URL, reverse('short_link', kwargs={'base62':self._hash}))

    @classmethod
    def get_or_create(cls, url):
        try:
            return Link.objects.get(url=url)
        except cls.DoesNotExist:
            return cls.create(url)

    @classmethod
    def create(cls, url):
        if cls.url_is_valid(url) == False:
            raise ValueError('Invalid URL')

        if LINK_UNIQUENESS and cls.link_exists(url) == True:
            raise ValueError('Link already exists')

        instance = cls()
        instance._hash = cls.generate_unique_hash(instance)
        instance.url = url

        instance.save()
        return instance

    @classmethod
    def generate_unique_hash(cls, instance):
        if HASH_STRATEGY is 'random':
            return cls.generate_unique_random_hash()
        else:
            instance.save() # To get an id.
            return base64.urlsafe_b64encode(base62.from_decimal(instance.id)).strip('=')


    @classmethod
    def generate_unique_random_hash(cls, i=0):
        hash_ = cls.generate_random_hash()
        if cls.hash_exists(hash_):
            if (i>=100):
                log.warn('Hashes are clashing, consider a new random factory.')
            return cls.generate_unique_random_hash(i=i+1)
        else:
            return hash_

    @classmethod
    def generate_random_hash(cls):
        return base64.urlsafe_b64encode(os.urandom(HASH_SEED_LENGTH)).strip('=')

    @classmethod
    def hash_exists(cls, hash_):
        try:
            row = Link.objects.get(_hash=hash_)
        except cls.DoesNotExist:
            return False
        else:
            return True

    @classmethod
    def link_exists(cls, url):
        try:
            row = Link.objects.get(url=url)
        except cls.DoesNotExist:
            return False
        else:
            return True

    @classmethod
    def url_is_valid(cls, url):
        validate = URLValidator()
        try:
            validate(url)
            return True
        except ValidationError:
            return False
