from django.contrib import admin

from gym.models import Gym, Province, City


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.TabularInline):
    model = City


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    inlines = [CityAdmin]
