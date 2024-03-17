from django.db import models
from django.conf import settings
from .events import Event

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
