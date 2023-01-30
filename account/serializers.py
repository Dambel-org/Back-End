from django.contrib.auth.models import update_last_login
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import *


class BaseUserSerializer(serializers.ModelSerializer):
    conf_password = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = BaseUser
        fields = ('email', 'first_name', 'last_name', 'age', 'password', 'conf_password')

    def create(self, validated_data):
        if validated_data['password'] != validated_data['conf_password']:
            raise serializers.ValidationError('Passwords do not match')
        conf_password = validated_data.pop('conf_password')
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
        fields = ('user', 'license_number', 'phone_number')

    def create(self, validated_data):
        user = validated_data.pop('user')
        number = validated_data.pop('phone_number')

        user = BaseUserSerializer().create(user)
        gym_owner = GymOwner.objects.create(user=user, **validated_data)
        GymOwnerPhoneNumber.objects.create(gym_owner=gym_owner, number=number)
        return gym_owner


class LoginGymOwnerSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        update_last_login(None, self.user)

        return data
