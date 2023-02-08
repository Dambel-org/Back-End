from rest_framework import serializers, status
from rest_framework.response import Response

from account.models import Trainee
from gym.models import TraineePreRegistration, GymTrainee


class TraineePreRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TraineePreRegistration
        fields = "__all__"

    def create(self, validated_data):
        return TraineePreRegistration.objects.create(**validated_data)


class GymTraineeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GymTrainee
        fields = "__all__"

    def create(self, validated_data):
        return GymTrainee.objects.create(**validated_data)

