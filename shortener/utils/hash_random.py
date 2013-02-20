#!/usr/bin/env python
# encoding: utf-8

import os
import base64
import logging

from shortener.models import Link

log = logging.getLogger(__name__)

def generate_random_hash(min_length, max_length):
    return base64.urlsafe_b64encode(os.urandom(max_length)).strip('=')

def generate_unique_random_hash(instance, min_length, max_length, i=0):
    hash = generate_random_hash(min_length, max_length)[:max_length]
    if Link.hash_exists(hash):
        if (i>=100):
            log.warn('Hashes are clashing, consider increasing max_hash_length.')
        return generate_unique_random_hash(instance, min_length, max_length, i=i+1)
    else:
        return hash
