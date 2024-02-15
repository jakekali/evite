from django.db import models
from django.conf import settings
from .events import Event

class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="invitations")

    def __str__(self):
        return f'Invitation for {self.event}'
    