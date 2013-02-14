import logging

from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

from chimp_shortener.models import Link
from chimp_shortener.signals import link_followed

log = logging.getLogger(__name__)

def follow(request, base62):
    link = get_object_or_404(Link, _hash = base62)
    link_followed.send_robust(sender=link, request=request)
    return HttpResponseRedirect(link.url)
