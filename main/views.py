from django.shortcuts import render
from rest_framework import mixins, status
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth import authenticate
import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework.response import Response
from serial import Serial
import random

ARDUINO_PORT = 'COM3'
ARDUINO_BAUDRATE = 9600

class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods = ["POST"], detail=False)
    def login(self, request):
        user_id = request.data.get("user_id")
        password = request.data.get("password")
        user = authenticate(user_id = user_id, password = password)
        if user is not None and user.is_active:
            expired_at = (timezone.now() + timedelta(days=14)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            access_token = jwt.encode(
                {"user_id":user.id, "expired_at":expired_at},settings.SECRET_KEY)
            return Response(access_token)
        return Response("유효하지 않은 정보입니다", status=status.HTTP_400_BAD_REQUEST)
    
    
class TemparatureHumidityViewSet(viewsets.ViewSet):
    def list(self, request):
        with Serial(ARDUINO_PORT, ARDUINO_BAUDRATE) as arduino:
            arduino.readline()
        
            data = arduino.readline().decode().strip()
            print(data)
            _, humdity, temperature = data.split(',')

        light = random.randint(0, 1023)
        humdity = int(humdity)
        temperature = int(temperature)

        return Response({
            'temperature' : temperature,
            'humidity' : humdity,
            'light' : light,
        })