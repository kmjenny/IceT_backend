from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    join_date = models.DateField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=15)
    point = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    illuminance = models.FloatField()
    soil_moisture = models.FloatField()