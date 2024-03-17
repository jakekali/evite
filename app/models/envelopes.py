from django.db import models
from django.conf import settings

class Envelope(models.Model):
    title_env = models.CharField(max_length=50)
    pattern_env = models.FilePathField(path="envelopes") # add imgs to envelopes dir