from django.contrib import admin

from gym.models import *


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    pass


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(TrainerInvitation)
class TrainerInvitationAdmin(admin.ModelAdmin):
    pass


@admin.register(MapLocation)
class LocationAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.TabularInline):
    model = City


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    inlines = [CityAdmin]


@admin.register(GymTrainer)
class GymTrainerAdmin(admin.ModelAdmin):
    pass


@admin.register(GymTrainee)
class GymTraineeAdmin(admin.ModelAdmin):
    pass


@admin.register(TraineeRequest)
class TraineeRequestAdmin(admin.ModelAdmin):
    pass
