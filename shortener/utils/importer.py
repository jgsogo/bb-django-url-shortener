#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.core.exceptions import  ImproperlyConfigured

def load_class(class_str):
    if isinstance(class_str, basestring):
        components = class_str.split('.')
        mod = __import__('.'.join(components[:-1]), fromlist=components[-1:])
        as_class = getattr(mod, components[-1:][0])
        return as_class
    else:
        raise ValueError("Argument must be a string")

def get_basemodel_mixin(basemodel_mixin):
    if isinstance(basemodel_mixin, basestring):
        as_model = load_class(basemodel_mixin)
        return get_basemodel_mixin(as_model)

    if issubclass(basemodel_mixin, models.Model) and basemodel_mixin._meta.abstract:
        return basemodel_mixin
    else:
        raise ImproperlyConfigured("'%s' must be an abstract django model." % basemodel_mixin)