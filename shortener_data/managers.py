from django.db import models
from django.db.models import Q

class RequestDataManager(models.Manager):
    def human(self):
        return self.filter(Q(user_agent__is_human=True))