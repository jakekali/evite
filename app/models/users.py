from django.db import models
from django.conf import settings

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()