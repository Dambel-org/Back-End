from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import Trainee, GymOwner
from gym.models import TraineePreRegistration, Gym, Invitation
from gym.permissions import IsGymOwner, IsTrainer

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


class GymListView(generics.ListAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['sport_filed', ]
    search_fields = ['name', ]


class GymDetailView(generics.RetrieveAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    lookup_field = 'gym_id'

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs['gym_id'])


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
        gym = self.kwargs['gym_id']
        if gym.gym_owner.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'plan created!'}, status=status.HTTP_201_CREATED)


class CreateInviteTrainersView(generics.CreateAPIView):
    queryset = Invitation.objects.all()
    permission_classes = [IsGymOwner]
    serializer_class = CreateInviteSerializer


class InvitationViewList(generics.ListAPIView):
    serializer_class = InviteSerializer

    def get_queryset(self):
        user = self.request.user
        trainer = Trainer.objects.get(user=user)
        return Invitation.objects.filter(trainer=trainer)


class AcceptInvitationByTrainer(generics.CreateAPIView):
    serializer_class = AcceptInviteSerializer
    permission_classes = [IsTrainer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'trainer added to gym successfully!'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)