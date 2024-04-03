from django.db import models
from django.conf import settings
from .events import Event
from .backgrounds import Background
from .envelopes import Envelope

class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True)
    envelope = models.ForeignKey(Envelope, on_delete=models.CASCADE, null=True)
    card = models.ImageField()
