from django.db import transaction
from rest_framework import serializers, status
from rest_framework.response import Response

from account.models import *
from gym.models import TraineePreRegistration, GymTrainee, Gym, City, Province


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('first_name', 'last_name')


class TraineeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainee
        fields = ('id', 'user', 'height', 'weight')

    def create(self, validated_data):
        user = validated_data['user']


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


class GymSerializer(serializers.ModelSerializer):
    gym_owner = GymOwnerSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Gym
        fields = ('name', 'description', 'gym_owner', 'city', 'address')


class CreateGymSerializer(serializers.ModelSerializer):
    city_id = serializers.IntegerField()

    class Meta:
        model = Gym
        fields = ('name', 'description', 'city_id', 'address')

    def create(self, validated_data):
        city = City.objects.get(pk=validated_data.pop('city_id'))
        gym_owner = GymOwner.objects.get(user=self.context['request'].user)
        gym = Gym.objects.create(gym_owner=gym_owner, city=city, **validated_data)
        return gym
