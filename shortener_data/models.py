import re
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from shortener.models import Link

from shortener_data.managers import RequestDataManager
from shortener_data.utils import UASparser

log = logging.getLogger(__name__)

HTTP_REGEX = re.compile('^HTTP_')
LINK_RE = re.compile(ur'\b(?:(?:https?)://|www\.)[-A-Z0-9+&@#/%=~_|$?!:,.]*[A-Z0-9+&@#/%=~_|$]', re.I|re.M)


class UserAgentType(models.Model):
    name = models.CharField(max_length=140)

    def __unicode__(self):
        return str(self.name)

class UserAgent(models.Model):
    user_agent_string = models.TextField()
    #_is_human = models.FloatField(default=1)
    _hit_robots = models.PositiveIntegerField(default=0)

    # User agent
    typ = models.ForeignKey(UserAgentType)
    name = models.CharField(max_length=255)
    family = models.CharField(max_length=255)
    url = models.URLField()
    company = models.CharField(max_length=255)
    company_url = models.URLField()
    icon = models.URLField()

    # Operating system
    os_name = models.CharField(max_length=255)
    os_family = models.CharField(max_length=255)
    os_url = models.URLField()
    os_company = models.CharField(max_length=255)
    os_company_url = models.URLField()
    os_icon = models.URLField()

    def __unicode__(self):
        return str(self.typ)

    @classmethod
    def create(cls, useragent_string, commit=True):
        try:
            instance = cls.objects.get(user_agent_string=useragent_string)
            return instance
        except cls.DoesNotExist:
            instance = cls(user_agent_string=useragent_string)
            try:
                uasparser = UASparser()
                ret = uasparser.parse(useragent_string)
                instance.typ, created = UserAgentType.objects.get_or_create(name=ret['typ'])
            except:
                pass
            finally:
                if commit:
                    instance.save()
            return instance

    @classmethod
    def on_robots(cls, useragent_string):
        instance = cls.create(useragent_string)
        instance._hit_robots = models.F('_hit_robots')+1
        instance.save()

    @property
    def is_human(self):
        # End user must be able to modify confidence interval
        return  (self.requestdata_set.count() > self._hit_robots)


class RequestData(models.Model):
    # http://devhttp.com/request/django
    link = models.ForeignKey(Link)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    accept = models.TextField()
    accept_encoding = models.CharField(max_length=255)
    accept_language = models.CharField(max_length=255)
    cache_control = models.CharField(max_length=255)
    connection = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    referer = models.URLField(_('referer'), max_length=500)
    via = models.CharField(max_length=255)
    x_forwarded_for = models.CharField(max_length=255)

    remote_addr = models.IPAddressField(_('IP address'))

    user_agent = models.ForeignKey(UserAgent)

    objects = RequestDataManager()

    class Meta:
        verbose_name = _('request')
        verbose_name_plural = _('requests')
        ordering = ('-datetime',)

    def __unicode__(self):
        return "[%s] %s" % (self.datetime, self.link)

    @classmethod
    def parse_request(cls, request):
        fields = [field.name for field in cls._meta.fields]
        # HTTP_
        headers = dict((header[5:].lower(), value) for (header, value) in request.META.items() if header.startswith('HTTP_') and header[5:].lower() in fields)

        # REMOTE_
        headers.update({'remote_addr' : request.META['REMOTE_ADDR']})
        return headers

    @classmethod
    def create(cls, request, link, commit=True):
        data = cls.parse_request(request)
        user_agent = data.pop('user_agent')
        request_data = cls(**data)
        request_data.user_agent = UserAgent.create(user_agent)
        request_data.link = link
        if commit:
            request_data.save()
        return request_data

    @property
    def is_human(self):
        return self.user_agent.is_human

Link.visits = property(lambda u: u.requestdata_set.human().count())

"""
    Signals
"""
from shortener.signals import link_followed

def on_request(sender, request, **kwargs):
    try:
        request_data = RequestData.create(request, sender, commit=False)
    except:
        request_data = RequestData()
        request_data.link = sender
    finally:
        request_data.save()

link_followed.connect(on_request)
