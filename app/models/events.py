from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail, send_mail

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    host = models.TextField(null=True)

    def __str__(self):
        return self.title
    
    def sendInvites(self):
      for guest in self.guest_set.all():
        guest.send_invitation()