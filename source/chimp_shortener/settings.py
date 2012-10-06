
from django.conf import settings

LINK_UNIQUENESS = getattr(settings, 'SHORTENER_LINK_UNIQUENESS', False)
LINK_VALIDATION = getattr(settings, 'SHORTENER_LINK_VALIDATION', False)

HASH_STRATEGY = getattr(settings, 'SHORTENER_HASH_STRATEGY', None)

HASH_SEED_LENGTH = getattr(settings, 'SHORTENER_HASH_SEED_LENGHT', 3)
SITE_BASE_URL = getattr(settings, 'SHORTENER_SITE_BASE_URL')
