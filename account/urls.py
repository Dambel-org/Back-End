from django.urls import path

from .views import *

urlpatterns = [
    path('signup/gymowner/', SignUpGymOwnerView.as_view(), name='gymowner-signup'),
    path('signup/trainee/', SignUpTraineeView.as_view(), name='trainee-signup'),
    path('signup/trainer/', SignUpTrainerView.as_view(), name='trainer-signup'),

    path('login/', LoginView.as_view(), name='login'),

    path('trainers/', TrainerListView.as_view(), name='trainer-list'),

    path('reset/', ForgotPasswordView.as_view(), name='reset-pass'),
    path('reset/confirm/', ResetPasswordView.as_view(), name='confirm-reset-pass'),
    path('check-code/', CheckVerificationCodeView.as_view(), name='check-code'),

    path('verify/', VerifyAccountView.as_view(), name='verify-account'),

    path('profile/', ProfileView.as_view(), name='profile')
]
