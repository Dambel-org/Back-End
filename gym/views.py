from math import sqrt
from urllib import response

from _decimal import Decimal
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import Trainee, GymOwner
from account.serializers import BaseUserSerializer
from gym.models import TraineePreRegistration, Gym, TrainerInvitation
from gym.permissions import IsGymOwner, IsTrainer, IsTrainee

from gym.serializers import *


class TraineePreRegistrationCreateView(generics.CreateAPIView):
    serializer_class = TraineePreRegistrationSerializer
    lookup_field = ['gym_id']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"gym_id": self.kwargs['gym_id']})
        return context

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'trainee pre-registration created!'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TraineePreRegistrationListView(generics.ListAPIView):
    serializer_class = TraineePreRegistrationSerializer
    permission_classes = [IsGymOwner, ]

    def get_queryset(self):
        user = self.request.user
        gym_owner = GymOwner.objects.get(user=user)
        return TraineePreRegistration.objects.filter(gym__gym_owner=gym_owner)


class SubmitTraineePreRegistrationView(generics.CreateAPIView):
    serializer_class = GymTraineeSerializer
    lookup_field = ['gym_id', 'trainee_id']
    permission_classes = [IsGymOwner, ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"gym_id": self.kwargs['gym_id'],
                        "trainee_id": self.kwargs['trainee_id']})

        return context

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'trainee registration completed successfully!'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GymCreateView(generics.CreateAPIView):
    queryset = Gym.objects.all()
    permission_classes = [IsGymOwner]
    serializer_class = CreateGymSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                city = City.objects.get(pk=validated_data.pop('city_id'))
                latitude = validated_data.pop('latitude')
                longitude = validated_data.pop('longitude')
                address = validated_data.pop('address')
                map_location = MapLocation.objects.create(latitude=latitude, longitude=longitude, address=address)
                gym_owner = GymOwner.objects.get(user=request.user)
                Gym.objects.create(gym_owner=gym_owner, city=city, location=map_location, **validated_data)
                return Response({'detail': 'gym created successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail' 'data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail : bad request!'}, status=status.HTTP_400_BAD_REQUEST)


class GymListView(generics.ListAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = []
    search_fields = ['name', 'plans__name']

    def get_queryset(self):
        latitude = self.request.GET.get('latitude', '')
        longitude = self.request.GET.get('longitude', '')
        r = self.request.GET.get('r', '')
        if latitude == '' and longitude == '':
            return Gym.objects.all()
        gyms = Gym.objects.all()
        result = []
        x = Decimal(latitude)
        y = Decimal(longitude)
        r = Decimal(r)
        for gym in gyms:
            gym_r = sqrt(
                (gym.location.latitude - x) ** 2 + (gym.location.longitude - y) ** 2)

            if gym_r <= r:
                result.append(gym)

        return result


class GymDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    lookup_field = 'gym_id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsGymOwner(), ]
        return [AllowAny(), ]

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs['gym_id'])


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsTrainee]
    serializer_class = CreateCommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'comment added successfully!'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProvinceListView(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class ProvinceDetailView(generics.RetrieveAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    lookup_field = ['province_id']

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs['province_id'])


class CreatePlanView(generics.CreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsGymOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"gym_id": self.kwargs['gym_id']})
        return context

    def post(self, request, *args, **kwargs):
        gym_id = self.kwargs['gym_id']
        gym = Gym.objects.get(pk=gym_id)
        if gym.gym_owner.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'plan created!'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateInviteTrainersView(generics.CreateAPIView):
    queryset = TrainerInvitation.objects.all()
    permission_classes = [IsGymOwner]
    serializer_class = CreateInviteSerializer


class InvitationViewList(generics.ListAPIView):
    serializer_class = InviteSerializer
    permission_classes = [IsTrainer, ]

    def get_queryset(self):
        user = self.request.user
        trainer = Trainer.objects.get(user=user)
        return TrainerInvitation.objects.filter(trainer=trainer)


class AcceptInvitationByTrainer(generics.CreateAPIView):
    serializer_class = AcceptInviteSerializer
    permission_classes = [IsTrainer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'trainer added to gym successfully!'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserGymView(generics.ListAPIView):
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated, ]

    def get_role(self):
        user = self.request.user
        trainee = Trainee.objects.filter(user=user)
        if len(trainee) == 1:
            return trainee[0]
        trainer = Trainer.objects.filter(user=user)
        if len(trainer) == 1:
            return trainer[0]
        gym_owner = GymOwner.objects.filter(user=user)
        if len(gym_owner) == 1:
            return gym_owner[0]

    def get_queryset(self):
        user_by_role = self.get_role()
        if isinstance(user_by_role, GymOwner):
            return Gym.objects.filter(gym_owner=user_by_role)
        if isinstance(user_by_role, Trainee):
            gym_trainees = GymTrainee.objects.filter(trainee=user_by_role)
            res = []
            for gt in gym_trainees:
                res.append(gt.gym)
            return res
        if isinstance(user_by_role, Trainer):
            gym_trainers = GymTrainer.objects.filter(trainer=user_by_role)
            res = []
            for gt in gym_trainers:
                res.append(gt.gym)
            return res


class TraineePlanView(APIView):
    permission_classes = [IsTrainee, ]

    def get(self, request, format=None):
        user = request.user
        trainee = Trainee.objects.get(user=user)
        plans = Plan.objects.filter(trainee=trainee)

        return Response(PlanSerializer(plans, many=True).data)


class RequestViewList(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsGymOwner, IsTrainee]

    def get_role(self):
        user = self.request.user
        trainee = Trainee.objects.filter(user=user)
        if len(trainee) == 1:
            return trainee[0]
        trainer = Trainer.objects.filter(user=user)
        if len(trainer) == 1:
            return trainer[0]
        gym_owner = GymOwner.objects.filter(user=user)
        if len(gym_owner) == 1:
            return gym_owner[0]

    def get_queryset(self):
        user_by_role = self.get_role()
        result = None
        if isinstance(user_by_role, GymOwner):
            plans = Plan.objects.filter(gym__gym_owner=user_by_role)
            result = TraineeRequest.objects.filter(plan__in=plans)
        elif isinstance(user_by_role, Trainee):
            result = TraineeRequest.objects.filter(trainee=user_by_role)
        return result


class CreateRequestTraineeView(generics.CreateAPIView):
    serializer_class = CreateRequestSerializer
    permission_classes = [IsTrainee, ]


class AcceptRequestByGymOwner(generics.CreateAPIView):
    serializer_class = AcceptRequestSerializer
    permission_classes = [IsGymOwner, ]


class GymUsersView(generics.ListAPIView):
    serializer_class = BaseUserSerializer
    permission_classes = [IsGymOwner]
    lookup_field = "gym_id"

    def get_queryset(self):
        gym_trainers = GymTrainer.objects.filter(gym_id=self.kwargs['gym_id'])
        gym_trainees = GymTrainee.objects.filter(gym_id=self.kwargs['gym_id'])
        result = []
        for gym_trainee in gym_trainees:
            result.append(gym_trainee.trainee.user)
        for gym_trainer in gym_trainers:
            result.append(gym_trainer.trainer.user)
        return result
