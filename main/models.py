from django.db import models

# Create your models here.
class Profile(models.Model):
    nickname = models.CharField(max_length=15)
    join_date = models.DateField()
    point = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    illuminance = models.FloatField()
    soil_moisture = models.FloatField()