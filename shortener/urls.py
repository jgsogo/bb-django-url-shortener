from django.conf.urls import patterns, include, url

from shortener.settings import WORKING_MODE
from shortener import MODES

if WORKING_MODE is MODES.redirects:
    from shortener.views import follow
    urlpatterns = patterns('',
        url(r'^(?P<base62>\w+)$', follow, name='short_link'),
        )

elif WORKING_MODE is MODES.shortener:
    urlpatterns = patterns('',

        )
