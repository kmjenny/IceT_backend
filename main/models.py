from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None):
        if not user_id:
            raise ValueError('아이디를 입력해주세요')
        user = self.model(
            user_id = user_id
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_id, password=None):
        user = self.create_user(
            user_id = user_id,
            password = password
        )
        user.is_staff=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, unique=True)
    join_date = models.DateField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'user_id'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=15, blank=True)
    point = models.IntegerField(blank=True, default=0)
    temperature = models.FloatField(blank=True, default=0)
    humidity = models.FloatField(blank=True, default=0)
    illuminance = models.FloatField(blank=True, default=0)
    soil_moisture = models.FloatField(blank=True, default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    mood = models.IntegerField()
    content = models.TextField()
    achievement_rate = models.FloatField(default=0)

class Mission(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    mission_id = models.IntegerField()
    content = models.CharField(max_length=100)
    condition = models.IntegerField()
    is_done = models.IntegerField(default=0)
    is_today= models.IntegerField(default=0)

@receiver(post_save, sender=Profile)
def create_mission(sender, instance, created, **kwargs):
    if created:
        mission1 = Mission.objects.create(
            profile = instance.user.profile,
            mission_id = 1,
            content = "흙에 물 주기",
            condition = 1,
            is_done = 0,
            is_today = 0
        )
        mission2 = Mission.objects.create(
            profile = instance.user.profile,
            mission_id = 2,
            content = "햇볕 드는 장소로 옮기기",
            condition = 2,
            is_done = 0,
            is_today = 0
        )
        mission3 = Mission.objects.create(
            profile = instance.user.profile,
            mission_id = 3,
            content = "그늘진 장소로 옮기기",
            condition = 3,
            is_done = 0,
            is_today = 0
        )
        mission4 = Mission.objects.create(
            profile = instance.user.profile,
            mission_id = 4,
            content = "실내로 식물 옮기기",
            condition = 4,
            is_done = 0,
            is_today = 0
        )
        mission5 = Mission.objects.create(
            profile = instance.user.profile,
            mission_id = 5,
            content = "식물 주변에 분무하기",
            condition = 5,
            is_done = 0,
            is_today = 0
        )
        mission6 = Mission.objects.create(
            profile = instance.user.profile,
            mission_id = 6,
            content = "떨어진 잎 정리하기",
            condition = 6,
            is_done = 0,
            is_today = 0
        )
        mission7 = Mission.objects.create(
            profile = instance.user.profile,
            mission_id = 7,
            content = "잎에 쌓인 먼지 닦기",
            condition = 6,
            is_done = 0,
            is_today = 0
        )
        mission8 = Mission.objects.create(
            profile = instance.user.profile,
            mission_id = 8,
            content = "가지치기",
            condition = 7,
            is_done = 0,
            is_today = 0
        )
        mission1.save()
        mission2.save()
        mission3.save()
        mission4.save()
        mission5.save()
        mission6.save()
        mission7.save()
        mission8.save()

class DayMission(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    is_done = models.IntegerField()
    date = models.DateField(auto_now_add=True)
