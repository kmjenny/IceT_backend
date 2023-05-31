from django.urls import include, path
from rest_framework import routers

from .views import *

profile_router = routers.SimpleRouter(trailing_slash = False)
profile_router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(profile_router.urls)),
]