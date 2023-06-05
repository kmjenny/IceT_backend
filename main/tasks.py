# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Mission, DayMission

@shared_task
def save_daily_missions():
    now = timezone.now()

    if now.minute == 0 and now.second == 0:
        # user = request.user
        # profile = Profile.objects.get(user=user)
        missions = Mission.objects.filter(profile = profile)
        missions = Mission.objects.filter(is_today=1)

        # DayMission에 저장
        for mission in missions:
            day_mission = DayMission(mission=mission)
            day_mission.save()
