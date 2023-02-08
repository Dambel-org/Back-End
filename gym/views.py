from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import Trainee
from gym.models import TraineePreRegistration
from gym.serializers import TraineePreRegistrationSerializer, GymTraineeSerializer


# class TraineePreRegisterCreateView(CreateAPIView):
#     serializer_class = TraineePreRegistrationSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TraineePreRegistrationView(generics.CreateAPIView):
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
            return Response({'trainee pre register created!'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TraineePreRegistrationSubmitView(APIView):
    def __get__(self, request, pk):
        trainee_pre_reg = TraineePreRegistration.objects.get(pk=pk)
        trainee_pre_reg.delete()
        serializer = GymTraineeSerializer(trainee_pre_reg)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
