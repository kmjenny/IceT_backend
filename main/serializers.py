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
        read_only_fields = ('user','point','temperature','humidity','illuminance','soil_moisture', 'user_id')
        fields = '__all__'

class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['join_date']

class MainSerializer(serializers.ModelSerializer):
    user = MainUserSerializer()

    class Meta:
        model = Profile
        fields = ['user','nickname','point', 'temperature', 'humidity', 'illuminance','soil_moisture']
    
class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        read_only_fields = ('user','date')
        fields = ['user', 'date', 'mood', 'content']

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'
