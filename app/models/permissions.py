from django.db import models
from django.conf import settings
from .users import User
from .events import Event

class Permissions(models.Model):
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
