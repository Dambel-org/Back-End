from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import Trainee, GymOwner
from gym.models import TraineePreRegistration
from gym.permissions import IsGymOwner
from gym.serializers import TraineePreRegistrationSerializer, GymTraineeSerializer


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


class GymPreRegistrationListView(generics.ListAPIView):
    serializer_class = TraineePreRegistrationSerializer
    permission_classes = [IsGymOwner, ]

    def get_queryset(self):
        user = self.request.user
        gym_owner = GymOwner.objects.get(user=user)
        return TraineePreRegistration.objects.filter(gym__gym_owner=gym_owner)


# class TraineePreRegistrationSubmitView(generics.CreateAPIView):
#     serializer_class = GymTraineeSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response({'trainee registration completed successfully!'}, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
