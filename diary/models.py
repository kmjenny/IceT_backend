from django.db import models

class Diary(models.Model):
    date = models.DateField()
    mood = models.IntegerField()
    content = models.TextField()
    achievement_rate = models.FloatField()