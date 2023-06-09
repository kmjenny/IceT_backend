from django.urls import include, path
from rest_framework import routers
from rest_framework import urls

from .views import *

profile_router = routers.SimpleRouter(trailing_slash = False)
profile_router.register("profiles", ProfileViewSet, basename="profiles")
user_router = routers.SimpleRouter(trailing_slash=False)
user_router.register("users", UserViewSet, basename="users")
diary_router = routers.SimpleRouter(trailing_slash=False)
diary_router.register("diaries", DiaryViewSet, basename="diaries")
mission_router = routers.SimpleRouter(trailing_slash=False)
mission_router.register("missions", MissionViewSet, basename="missions")

urlpatterns = [
    path("", include(profile_router.urls)),
    path("", include(user_router.urls)),
    path("", include(diary_router.urls)),
    path("", include(mission_router.urls)),
    path("profiles/<int:id>/", include(mission_router.urls)),
]