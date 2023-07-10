from django.contrib.auth.models import update_last_login
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        exclude = ["password", ]


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'password')

    def create(self, validated_data):
        user = BaseUser.objects.create_user(**validated_data)
        return user


class SignupGymOwnerSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = GymOwner
        fields = ('user',)

    @transaction.atomic()
    def create(self, validated_data):
        user = validated_data.pop('user')

        user = BaseUserSerializer().create(user)
        gym_owner = GymOwner.objects.create(user=user, **validated_data)
        GymOwnerPhoneNumber.objects.create(gym_owner=gym_owner)
        return gym_owner


class SignupTraineeSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Trainee
        fields = ('user', 'height', 'weight')

    @transaction.atomic()
    def create(self, validated_data):
        user = validated_data.pop('user')

        user = BaseUserSerializer().create(user)
        trainee = Trainee.objects.create(user=user, **validated_data)
        return trainee


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('number',)


class SignUpTrainerSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Trainer
        fields = ('user',)

    @transaction.atomic()
    def create(self, validated_data):
        user = validated_data.pop('user')
        user = BaseUserSerializer().create(user)
        trainer = Trainer.objects.create(user=user)
        return trainer


class TrainerSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Trainer
        fields = ('id', 'user')


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


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CheckVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    pass_1 = serializers.CharField(max_length=30)
    pass_2 = serializers.CharField(max_length=30)


class VerifyAccountSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
