from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, status, viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action, permission_classes
from django.contrib.auth import authenticate
import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework.response import Response
from serial import Serial
import random
from rest_framework.permissions import IsAuthenticated

ARDUINO_PORT = 'COM3'
ARDUINO_BAUDRATE = 9600

class ProfileViewSet(
    viewsets.ModelViewSet,
	viewsets.GenericViewSet
):
    serializer_class = MainSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    @action(methods=["PATCH"], detail=True)
    @permission_classes([IsAuthenticated])
    def profile_update(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    # @action(methods=["GET"], detail=True)
    # @permission_classes([IsAuthenticated])
    # def show_main(self, request):
    #     user = request.user
    #     profile = Profile.objects.get(user=user)
    #     serializer = MainSerializer(profile, data=request.data)
    #     return Response(serializer.data)

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
                {"just_id":user.id, "expired_at":expired_at},settings.SECRET_KEY)
            return Response(access_token)
        return Response("유효하지 않은 정보입니다", status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=["GET"], detail=False)
    @permission_classes([IsAuthenticated])
    def test(self, request):
        return Response(request.user.user_id)
    
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