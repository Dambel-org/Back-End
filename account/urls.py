from django.urls import path

from .views import *

urlpatterns = [
    path('signup/gymowner', SignUpGymOwnerView.as_view(), name='gymowner-signup'),
    path('signup/trainee', SignUpTraineeView.as_view(), name='trainee-signup'),
    path('signup/trainer', SignUpTrainerView.as_view(), name='trainer-signup'),
    path('login/', LoginView.as_view(), name='login'),
]
