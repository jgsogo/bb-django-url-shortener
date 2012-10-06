from django.conf.urls import patterns, include, url

from chimp_shortener.views import follow

urlpatterns = patterns('',
    url(r'^(?P<base62>\w+)$', follow, name='short_link'),
    )
