from rest_framework.permissions import BasePermission

from account.models import *


class IsGymOwner(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            gym_owner = GymOwner.objects.filter(user=user)
            if len(gym_owner) == 1:
                return True
        return False


class IsTrainer(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            trainer = Trainer.objects.filter(user=user)
            if len(trainer) == 1:
                return True
        return False


class IsTrainee(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            trainee = Trainee.objects.filter(user=user)
            if len(trainee) == 1:
                return True
        return False
