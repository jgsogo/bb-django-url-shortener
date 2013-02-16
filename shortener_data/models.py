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
    name = models.CharField(max_length=140)
    family = models.CharField(max_length=140)
    url = models.URLField()
    company = models.CharField(max_length=140)
    company_url = models.URLField()
    icon = models.URLField()

    # Operating system
    os_name = models.CharField(max_length=140)
    os_family = models.CharField(max_length=140)
    os_url = models.URLField()
    os_company = models.CharField(max_length=140)
    os_company_url = models.URLField()
    os_icon = models.URLField()

    def __unicode__(self):
        return str(self.typ)

    @classmethod
    def create(cls, useragent_string, commit=True):
        instance, created = cls.objects.get_or_create(user_agent_string=useragent_string)
        if created:
            try:
                uasparser = UASparser()
                ret = uasparser.parse(instance.user_agent_string)
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
        instance._hit_robots = F('_hit_robots')+1
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
    accept_encoding = models.CharField(max_length=140)
    accept_language = models.CharField(max_length=140)
    cache_control = models.CharField(max_length=140)
    connection = models.CharField(max_length=140)
    host = models.CharField(max_length=140)
    referer = models.CharField(max_length=500)
    user_agent = models.CharField(max_length=140)
    via = models.CharField(max_length=140)
    x_forwarded_for = models.CharField(max_length=140)

    remote_addr = models.CharField(max_length=15)

    user_agent = models.ForeignKey(UserAgent)

    objects = RequestDataManager()

    class Meta:
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')

    @classmethod
    def parse_request(cls, request):
        fields = [field.name for field in cls._meta.fields]
        # HTTP_
        headers = dict((header[5:].lower(), value) for (header, value) in request.META.items() if header.startswith('HTTP_') and header[5:].lower() in fields)

        # REMOTE_
        headers.update({'remote_addr' : request.META['REMOTE_ADDR']})
        return headers

    @classmethod
    def create(cls, request, link):
        data = cls.parse_request(request)
        request_data = cls(**data)
        request_data.user_agent = UserAgent.create(request.META['HTTP_USER_AGENT'])
        request_data.link = link
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
        request_data = RequestData.create(request, sender)
    except:
        request_data = RequestData()
    request_data.link = sender
    request_data.save()

link_followed.connect(on_request)
