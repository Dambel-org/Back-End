import json
from abc import ABC

from django.db import transaction
from rest_framework import serializers, status
from rest_framework.response import Response

from account.models import *
from account.serializers import TrainerSerializer

from gym.models import TraineePreRegistration, GymTrainee, Gym, City, Province, Invitation, GymTrainer, MapLocation, \
    Plan, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('first_name', 'last_name')


class TraineeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainee
        fields = ('id', 'user', 'height', 'weight')


class TraineePreRegistrationSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer()

    class Meta:
        model = TraineePreRegistration
        fields = ('trainee', 'gym')

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


class GymTraineeSerializer(serializers.Serializer):

    @transaction.atomic()
    def create(self, validated_data):
        gym_id = self.context['gym_id']
        trainee_id = self.context['trainee_id']
        TraineePreRegistration.objects.get(gym_id=gym_id, trainee_id=trainee_id).delete()
        gym_trainee = GymTrainee.objects.create(gym_id=gym_id, trainee_id=trainee_id)
        return gym_trainee


class GymOwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GymOwner
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class ProvinceSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=True)

    class Meta:
        model = Province
        fields = ('id', 'name', 'city')


class MapLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLocation
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer()

    class Meta:
        model = Comment
        fields = ['trainee', 'rate', 'text']


class PlanSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)

    class Meta:
        model = Plan
        exclude = ['gym', ]

    def create(self, validated_data):
        gym_id = self.context['gym_id']
        plan = Plan.objects.create(gym=gym_id, **validated_data)
        return plan


class GymSerializer(serializers.ModelSerializer):
    gym_owner = GymOwnerSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    location = MapLocationSerializer(read_only=True)
    plans = PlanSerializer(many=True)
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Gym
        fields = (
            'id', 'name', 'logo_image', 'background_image', 'description', 'gym_owner', 'city', 'contacts', 'location',
            'plans', 'rate')

    def get_rate(self, obj):
        comments = Comment.objects.filter(plan__gym=obj)
        rate = 0
        for comment in comments:
            rate += comment.rate
        if rate != 0:
            rate = round(rate / len(comments), 2)
        return rate


class CreateGymSerializer(serializers.Serializer):
    city_id = serializers.IntegerField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    address = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=100)
    logo_image = serializers.ImageField()
    background_image = serializers.ImageField()
    license_image = serializers.ImageField()
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    contacts = serializers.CharField(style={'base_template': 'textarea.html'})


class CreateCommentSerializer(serializers.ModelSerializer):
    plan = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['plan', 'rate', 'text']

    def create(self, validated_data):
        plan_id = validated_data.pop('plan')
        plan = Plan.objects.get(id=plan_id)
        user = self.context['request'].user
        trainee = Trainee.objects.get(user=user)
        comment = Comment.objects.create(trainee=trainee, plan=plan, **validated_data)
        return comment


class InviteSerializer(serializers.ModelSerializer):
    gym = GymSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ('gym', 'created_at')


class CreateInviteSerializer(serializers.Serializer):
    gym_id = serializers.IntegerField()
    trainer_id = serializers.IntegerField()

    def create(self, validated_data):
        gym = Gym.objects.get(pk=validated_data.pop('gym_id'))
        trainer = Trainer.objects.get(pk=validated_data.pop('trainer_id'))
        invitation = Invitation.objects.create(gym=gym, trainer=trainer, **validated_data)
        return invitation


class AcceptInviteSerializer(serializers.Serializer):
    gym_id = serializers.IntegerField()

    @transaction.atomic()
    def create(self, validated_data):
        gym_id = validated_data.pop('gym_id')
        trainer = Trainer.objects.get(user=self.context['request'].user)
        Invitation.objects.get(gym_id=gym_id, trainer=trainer).delete()
        gym_trainer = GymTrainer.objects.create(gym_id=gym_id, trainer=trainer)
        return gym_trainer
