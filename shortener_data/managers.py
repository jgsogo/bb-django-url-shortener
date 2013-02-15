from django.db import models
from django.db.models import Q

class RequestDataManager(models.Manager):
    def human(self):
        return self.filter(Q(user_agent_type__is_human=True), Q(user_agent_has_url=False))