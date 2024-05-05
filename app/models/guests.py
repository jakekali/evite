from typing import Any
from django.db import models
from django.conf import settings
from .events import Event
from django.core.mail import send_mail

# def _createHash():
#     return hexlify(os.urandom(5))
    
class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True, blank=True)      # is there better way? theres a phone number field pkg that exists if we want giggle
    address = models.CharField(max_length=200, null=True, blank=True)
    rsvp = models.BooleanField(null=True, default=None)
    history = models.JSONField(null=True)
    hash = models.CharField(max_length=10,default=4,unique=True)
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'email'], name='unique_guest'
            )
        ]
    def sendMassEmail(self, event, subject, message, from_email):
        message = (
            subject, message, from_email, []
        )