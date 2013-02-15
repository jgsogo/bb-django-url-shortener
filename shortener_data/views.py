import re

from chimp_shortener_data.models import UserAgentType, LINK_RE
from chimp_shortener_data.utils import UASparser

def robots(request):
    uasparser = UASparser()
    ret = uasparser.parse(request.META['HTTP_USER_AGENT'])
    user_agent_type, created = UserAgentType.objects.get_or_create(name=ret['typ'])
    user_agent_has_url = True if re.search(LINK_RE, request.META['HTTP_USER_AGENT']) else False