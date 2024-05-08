from django.db import models
from django.conf import settings

class Background(models.Model):
    backgroud_names = models.CharField(max_length=500)
    file = models.ImageField(upload_to='backgrounds/')

# add in initial backgrounds from admin panel on create