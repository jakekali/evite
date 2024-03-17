from django.db import models
from django.conf import settings

class Background(models.Model):
    title_bg = models.CharField(max_length=50)
    pattern_bg = models.FilePathField(path="backgrounds") # add imgs to backgrounds dir