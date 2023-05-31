from django.db import models

class Mission(models.Model):
    mission_id = models.IntegerField()
    is_done = models.IntegerField()

class AllMission(models.Model):
    content = models.CharField(max_length=100)