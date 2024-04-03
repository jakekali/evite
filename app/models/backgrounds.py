from django.db import models
from django.conf import settings

class Background(models.Model):
    title_bg = models.CharField(max_length=500)
    pattern_bg = models.CharField()

# add in initial backgrounds from admin panel on create