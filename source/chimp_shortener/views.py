from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect

from chimp_shortener.models import Link
from chimp_shortener.signals import link_followed

def follow(request, base62_id):
    link = get_object_or_404(Link, _hash = base62_id)
    link_followed.send(sender=link, request=request)
    return HttpResponsePermanentRedirect(link.url)
