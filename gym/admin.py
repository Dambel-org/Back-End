from django.contrib import admin

from gym.models import Gym


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    pass
