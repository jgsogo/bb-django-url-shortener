
from django.http import HttpResponse

from shortener_data.models import UserAgent
from shortener_data.settings import ROBOTS_FILEPATH

def robots(request):
    UserAgent.on_robots(request.META['HTTP_USER_AGENT'])
    robots_str = "User-agent: *\nDisallow: /\n"
    if ROBOTS_FILEPATH:
        try:
            robots_str = open(ROBOTS_FILEPATH, 'r').read()
        except IOError:
            pass
    return HttpResponse(robots_str, mimetype="text/plain")


