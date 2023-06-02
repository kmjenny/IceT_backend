from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            user_id = validated_data['user_id'],
            password = validated_data['password']
        )
        return user
    class Meta:
        model = User
        fields = ['user_id', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['nickname','point','temperature','humidity','illuminance','soil_moisture']