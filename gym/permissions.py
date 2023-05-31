from rest_framework.permissions import BasePermission

from account.models import *


class IsGymOwner(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if GymOwner.objects.get(user=user):
                return True
        return False


class IsTrainer(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if Trainer.objects.get(user=user):
                return True
        return False
