
import logging

from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from shortener.settings import LINK_UNIQUENESS, SITE_BASE_URL, HASH_STRATEGY, LINK_MIXIN, MAX_HASH_LENGTH
from shortener.utils.baseconv import base62
from shortener.utils import get_basemodel_mixin

log = logging.getLogger(__name__)

class BaseLink(models.Model):
    baseconverter = base62

    _hash = models.CharField(max_length=MAX_HASH_LENGTH, unique=True) # n-char unique random string
    url = models.CharField(max_length=2083) # http://www.boutell.com/newfaq/misc/urllength.html

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % self.url

    def get_short_link(self):
        return u'%s/%s' % (SITE_BASE_URL, self._hash)

    @classmethod
    def get_or_create(cls, url):
        try:
            return cls.objects.get(url=url)
        except cls.DoesNotExist:
            return cls.create(url)

    @classmethod
    def create(cls, url, commit=True):
        log.debug("Link::create(url='%s')" % url)
        if not cls.url_is_valid(url):
            raise ValueError('Invalid URL')

        if LINK_UNIQUENESS and cls.link_exists(url) == True:
            raise ValueError('Link already exists')

        instance = cls()
        instance._hash = cls.generate_unique_hash(instance)
        instance.url = url

        if commit:
            instance.save()
        return instance

    @classmethod
    def generate_unique_hash(cls, instance):
        if HASH_STRATEGY:
            hash = HASH_STRATEGY(instance, MAX_HASH_LENGTH)
            if cls.hash_exists(hash):
                raise ValueError("Generated hash already exists")
            return hash
        else:
            if not instance.id:
                instance.save() # To get an id.
            return cls.baseconverter.from_decimal(instance.id)

    @classmethod
    def hash_exists(cls, hash_):
        return cls.objects.filter(_hash=hash_).exists()

    @classmethod
    def link_exists(cls, url):
        return cls.objects.filter(url=url).exists()

    @classmethod
    def url_is_valid(cls, url):
        try:
            URLValidator()(url)
            return True
        except ValidationError:
            return False


if LINK_MIXIN:
    Mixin = get_basemodel_mixin(LINK_MIXIN)
    class Link(Mixin, BaseLink):
        class Meta(Mixin.Meta):
            abstract = False

else:
    class Link(BaseLink):
        class Meta:
            abstract = False
