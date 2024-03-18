from django.db import models
from django.conf import settings
from .events import Event

class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True, blank=True)      # is there better way? theres a phone number field pkg that exists if we want giggle
    address = models.CharField(max_length=200, null=True, blank=True)
    rsvp = models.BooleanField(null=True, default=None)
    history = models.JSONField(null=True)
    hash = models.CharField(max_length=200, null=True, blank=True)