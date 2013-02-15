from django.conf.urls import patterns, include, url

from chimp_shortener.settings import WORKING_MODE
from chimp_shortener import MODES

if WORKING_MODE is MODES.redirects:
    from chimp_shortener.views import follow
    urlpatterns = patterns('',
        url(r'^(?P<base62>\w+)$', follow, name='short_link'),
        )

elif WORKING_MODE is MODES.shortener:
    urlpatterns = patterns('',

        )
