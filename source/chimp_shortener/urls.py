from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<base62_id>\w+)$', 'chimp_shortener.views.follow'),
)
