from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
    nickname = models.CharField(max_length=15)
    point = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    illuminance = models.FloatField()
    soil_moisture = models.FloatField()