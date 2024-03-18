from django.db import models
from django.conf import settings
from .users import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    host = models.TextField(null=True)

    def __str__(self):
        return self.title
