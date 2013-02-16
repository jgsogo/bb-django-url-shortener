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
    is_human = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class RequestData(models.Model):
    # http://devhttp.com/request/django
    link = models.ForeignKey(Link)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    meta = models.TextField()
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

    user_agent_type = models.ForeignKey(UserAgentType)
    user_agent_has_url = models.BooleanField(default=False)

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


"""
    Signals
"""
from shortener.signals import link_followed

def on_request(sender, request, **kwargs):
    try:
        data = RequestData.parse_request(request)
        request_data = RequestData(**data)
        uasparser = UASparser()
        ret = uasparser.parse(request.META['HTTP_USER_AGENT'])
        request_data.user_agent_type, created = UserAgentType.objects.get_or_create(name=ret['typ'])
        #request_data.user_agent_url = ret['ua_url']
        request_data.user_agent_has_url = True if re.search(LINK_RE, request.META['HTTP_USER_AGENT']) else False
    except:
        request_data = RequestData()
    request_data.link = sender
    request_data.save()

link_followed.connect(on_request)
