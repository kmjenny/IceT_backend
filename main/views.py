from django.shortcuts import render
from rest_framework import mixins
from .models import *
from .serializers import *
from rest_framework import viewsets
# Create your views here.

class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
