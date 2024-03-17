from django.db import models
from django.conf import settings
from .users import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    host = models.TextField()

    def __str__(self):
        return self.title
