from django.contrib import admin

from account.models import *


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    pass


@admin.register(GymOwner)
class TraineeAdmin(admin.ModelAdmin):
    pass


@admin.register(Trainer)
class TraineeAdmin(admin.ModelAdmin):
    pass


@admin.register(PhoneNumber)
class TraineeAdmin(admin.ModelAdmin):
    pass
