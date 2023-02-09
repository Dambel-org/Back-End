from django.db import transaction
from rest_framework import serializers, status
from rest_framework.response import Response

from account.models import *
from gym.models import TraineePreRegistration, TrainerPreRegistration, GymTrainee, GymTrainer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('first_name', 'last_name', 'email', 'password',)


class TraineeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainee
        fields = ('user', 'height', 'weight')


class TraineePreRegistrationSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer()

    class Meta:
        model = TraineePreRegistration
        fields = ('trainee',)

    @transaction.atomic()
    def create(self, validated_data):
        first_name = validated_data.get('trainee').get('user').get('first_name')
        last_name = validated_data.get('trainee').get('user').get('last_name')
        email = validated_data.get('trainee').get('user').get('email')
        password = validated_data.get('trainee').get('user').get('password')
        height = validated_data.get('trainee').get('height')
        weight = validated_data.get('trainee').get('weight')
        user = BaseUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        trainee = Trainee.objects.create(user=user, height=height, weight=weight)
        pre_reg = TraineePreRegistration.objects.create(trainee=trainee, gym_id=self.context['gym_id'])
        return pre_reg


class GymTraineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymTrainee
        fields = "__all__"

    def create(self, validated_data):
        return GymTrainee.objects.create(**validated_data)


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('number', )


class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    phone_number = PhoneNumberSerializer()

    class Meta:
        model = Trainer
        fields = ('user', 'phone_number', )


class TrainerPreRegistrationSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer()

    class Meta:
        model = TrainerPreRegistration
        fields = ('trainer', )

    @transaction.atomic()
    def create(self, validated_data):
        first_name = validated_data.get('trainer').get('user').get('first_name')
        last_name = validated_data.get('trainer').get('user').get('last_name')
        email = validated_data.get('trainer').get('user').get('email')
        password = validated_data.get('trainer').get('user').get('password')
        phone_number = validated_data.get('trainer').get('phone_number')
        user = BaseUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        trainer = Trainer.objects.create(user=user, phone_number=phone_number)
        pre_reg = TrainerPreRegistration.objects.create(trainer=trainer, gym_id=self.context['gym_id'])
        return pre_reg


class GymTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymTrainer
        fields = "__all__"

    def create(self, validated_data):
        return GymTrainer.objects.create(**validated_data)
