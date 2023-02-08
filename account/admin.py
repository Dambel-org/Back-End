from django.contrib import admin

from account.models import *


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    pass
