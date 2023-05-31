from django.db import models
from main.models import *

class Diary(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField()
    mood = models.IntegerField()
    content = models.TextField()
    achievement_rate = models.FloatField()