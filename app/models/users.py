from django.db import models
from django.conf import settings

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_and_email'
            )
        ]