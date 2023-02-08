from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from gym.models import TraineePreRegistration
from gym.serializers import TraineePreRegistrationSerializer, GymTraineeSerializer


class TraineePreRegisterCreateView(CreateAPIView):
    serializer_class = TraineePreRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TraineePreRegistrationView(APIView):
    def __get__(self, request, pk):
        trainee_pre_reg = TraineePreRegistration.objects.get(pk=pk)
        serializer = TraineePreRegistrationSerializer(trainee_pre_reg)
        return Response(serializer)

    def __delete__(self, request, pk):
        trainee_pre_reg = TraineePreRegistration.objects.get(pk)
        trainee_pre_reg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TraineePreRegistrationSubmitView(APIView):
    def __get__(self, request, pk):
        trainee_pre_reg = TraineePreRegistration.objects.get(pk=pk)
        trainee_pre_reg.delete()
        serializer = GymTraineeSerializer(trainee_pre_reg)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
