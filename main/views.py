from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, status, viewsets, permissions
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
	viewsets.GenericViewSet,
    viewsets.ViewSet
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
    
    @action(methods=["GET"], detail=True)
    @permission_classes([IsAuthenticated])
    def show_main(self, request, pk = None):
        user = request.user
        profile = Profile.objects.get(user=user)

        #with Serial(ARDUINO_PORT, ARDUINO_BAUDRATE) as arduino:
        #     arduino.readline()
        
        #     data = arduino.readline().decode().strip()
        #     _, humidity, temperature = data.split(',')
        
        illuminance = random.randint(0, 1023)
        soil_moisture = random.randint(0, 100)
        # humidity = int(humidity)
        # temperature = int(temperature)
        profile.illuminance = illuminance
        profile.soil_moisture = soil_moisture
        # profile.humidity = humidity
        # profile.temperature = temperature

        profile.save()
        serializer = MainSerializer(profile)
        return Response(serializer.data)

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
            expired_at = (timezone.now() + timedelta(days=140)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            access_token = jwt.encode(
                {"just_id":user.id, "expired_at":expired_at},settings.SECRET_KEY)
            response_data = {
                'access_token' : access_token
            }
            return Response(response_data)
        return Response("유효하지 않은 정보입니다", status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=["GET"], detail=False)
    @permission_classes([IsAuthenticated])
    def test(self, request):
        return Response(request.user.user_id)

class DiaryViewSet(viewsets.ModelViewSet,viewsets.GenericViewSet):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Diary.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class MissionViewSet(viewsets.ModelViewSet, viewsets.GenericViewSet):
    serializer_class = MissionSerializer

    @permission_classes([IsAuthenticated])
    def get_queryset(self, *args, **kwargs):
        queryset = Mission.objects.filter(
            profile = self.kwargs.get("id")
        )
        return queryset
    
    @permission_classes([IsAuthenticated])
    @action(methods=["GET"], detail=False)
    def mission_set(self, request, id=None):
        user = request.user
        profile = Profile.objects.get(user=user)
        missions = Mission.objects.filter(profile = profile)

        temperature = profile.temperature
        humidity = profile.humidity
        illuminance = profile.illuminance
        soil_moisture = profile.soil_moisture

        day = timezone.now().day
        month = timezone.now().month

        for mission in missions:
            mission_id = mission.mission_id
            
            if soil_moisture<=40:
                if mission_id == 1:
                    mission.is_today = 1
            
            if illuminance <= 300:
                if mission_id == 2:
                    mission.is_today = 1
            elif illuminance >= 1000:
                if mission_id == 3:
                    mission.is_today = 1
            
            if temperature <= 10:
                if mission_id == 4:
                    mission.is_today = 1
            if humidity <= 40:
                if mission_id == 5:
                    mission.is_today = 1

            if day == 1:
                if mission_id == 6:
                    mission.is_today = 1
                
                if mission_id == 7:
                    mission.is_today = 1
            
            if month == 6 or month == 8 or month == 12:
                if day == 5:
                    if mission_id == 8:
                        mission.is_today = 1

            mission.save()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data)
    
    @permission_classes([IsAuthenticated])
    @action(methods=["GET"], detail=False)
    def mission_check(self, request, id=None):
        user = request.user
        profile = Profile.objects.get(user=user)
        missions = Mission.objects.filter(profile = profile)

        temperature = profile.temperature
        humidity = profile.humidity
        illuminance = profile.illuminance
        soil_moisture = profile.soil_moisture

        day = timezone.now().day
        month = timezone.now().month

        for mission in missions:
            mission_id = mission.mission_id
            
            if soil_moisture>40:
                if mission_id == 1:
                    mission.is_done = 1
            
            if illuminance > 300:
                if mission_id == 2:
                    mission.is_done = 1
            
            if illuminance < 1000:
                if mission_id == 3:
                    mission.is_done = 1
            
            if temperature > 10:
                if mission_id == 4:
                    mission.is_done = 1
            if humidity > 40:
                if mission_id == 5:
                    mission.is_done = 1

            mission.save()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data)