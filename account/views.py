from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import *


class SignUpGymOwnerView(CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = SignupGymOwnerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SignUpTraineeView(CreateAPIView):
    queryset = Trainee.objects.all()
    serializer_class = SignupTraineeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SignUpTrainerView(CreateAPIView):
    queryset = Trainer.objects.all()
    serializer_class = SignUpTrainerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(TokenObtainPairView):
    queryset = BaseUser.objects.all()
    serializer_class = MyTokenObtainPairSerializer


class TrainerListView(generics.ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
