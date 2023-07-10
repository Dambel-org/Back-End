import base64
import random
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
# from django.core.mail import send_mail
from Dambel.function_utils import send_email
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from googleapiclient.discovery import build
from google.oauth2 import service_account
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


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
    filter_backends = [SearchFilter]
    search_fields = ['user__first_name', 'user__last_name']


# class GymUsersView(generics.ListAPIView):


class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        # Check if the email exists in the database
        try:
            user = BaseUser.objects.get(email=email)
        except BaseUser.DoesNotExist:
            return Response({'detail': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a 6-digit code
        code = random.randint(100000, 999999)

        # Save the code to the user model
        user.reset_code = code
        user.save()

        subject = 'Password Reset Request'
        message = f"""
Hi {user.first_name},

There was a request to change your password!

If you did not make this request then please ignore this email.


Otherwise, please back to the website and complete your reset password.

Verification Code : {code}
        """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        # send_mail(subject, message, email_from, recipient_list, fail_silently=True)
        send_email(subject, message, recipient_list)
        return Response({'detail': 'Email sent successfully!'}, status=status.HTTP_201_CREATED)


class CheckVerificationCodeView(generics.CreateAPIView):
    serializer_class = CheckVerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = BaseUser.objects.get(email=email)
        except BaseUser.DoesNotExist:
            return Response({'detail': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)
        if str(user.reset_code) != str(code):
            return Response({'detail': 'the code is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'the code is correct'}, status=status.HTTP_200_OK)


class ResetPasswordView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        pass_1 = request.data.get('pass_1')
        pass_2 = request.data.get('pass_2')

        try:
            if pass_1 != pass_2:
                return Response({'detail': 'password doesnt match!'}, status=status.HTTP_400_BAD_REQUEST)
            user = BaseUser.objects.get(email=email)

            if str(user.reset_code) == str(code):
                user.set_password(pass_1)
                user.reset_code = None
                user.save()
                return Response({'detail': 'password changed successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'bad request.'}, status=status.HTTP_404_NOT_FOUND)


class VerifyAccountView(APIView):
    serializer_class = VerifyAccountSerializer

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            return Response({'detail: please login first'}, status=status.HTTP_400_BAD_REQUEST)
        if user.verified:
            return Response({'detail': 'Account already activated!'}, status=status.HTTP_200_OK)
        # Save the code to the user model
        code = random.randint(100000, 999999)
        user.verify_code = code
        user.save()

        subject = 'Verification Account'
        message = f"""
Hi {user.first_name}!

Your verification code is {code}.

Enter this code in our website to activate your account.

We’re glad you’re here!
Dambel team
                """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list, fail_silently=True)

        return Response({'detail': 'Email sent successfully!'}, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        if str(user.verify_code) == str(code):
            user.verified = True
            user.verify_code = None
            user.save()
            return Response({'detail': 'Account activated successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        pk = request.user.pk
        user = BaseUser.objects.get(pk=pk)
        return Response(ProfileSerializer(user).data)
