from django.contrib.auth.models import update_last_login
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import *


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = BaseUser.objects.create_user(**validated_data)
        return user


class GymOwnerPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymOwnerPhoneNumber
        fields = ('number',)


class SignupGymOwnerSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()
    phone_number = serializers.CharField(max_length=11, write_only=True)

    class Meta:
        model = GymOwner
        fields = ('user', 'phone_number')

    @transaction.atomic()
    def create(self, validated_data):
        user = validated_data.pop('user')
        number = validated_data.pop('phone_number')

        user = BaseUserSerializer().create(user)
        gym_owner = GymOwner.objects.create(user=user, **validated_data)
        GymOwnerPhoneNumber.objects.create(gym_owner=gym_owner, number=number)
        return gym_owner


class SignupTraineeSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()
    phone_number = serializers.CharField(max_length=11, write_only=True)

    class Meta:
        model = Trainee
        fields = ('user', 'phone_number', 'height', 'weight')

    @transaction.atomic()
    def create(self, validated_data):
        user = validated_data.pop('user')
        number = validated_data.pop('phone_number')

        user = BaseUserSerializer().create(user)
        trainee = Trainee.objects.create(user=user, **validated_data)
        TraineePhoneNumber.objects.create(trainee=trainee, number=number)
        return trainee


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('number',)


class SignUpTrainerSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()
    phone_number = PhoneNumberSerializer()

    class Meta:
        model = Trainer
        fields = ('user', 'phone_number')

    @transaction.atomic()
    def create(self, validated_data):
        user = validated_data.pop('user')
        number = validated_data.pop('phone_number')

        user = BaseUserSerializer().create(user)
        phone_number = PhoneNumberSerializer().create(number)

        trainer = Trainer.objects.create(user=user, phone_number=phone_number)
        return trainer


class TrainerSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()
    phone_number = PhoneNumberSerializer()

    class Meta:
        model = Trainer
        fields = ('user', 'phone_number')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if GymOwner.objects.filter(user=self.user).exists():
            data['role'] = 'GymOwner'
        elif Trainee.objects.filter(user=self.user).exists():
            data['role'] = 'Trainee'
        elif Trainer.objects.filter(user=self.user).exists():
            data['role'] = 'Trainer'
        return data
