from django.urls import path

from .views import *

urlpatterns = [
    path('gym-owner/signup/', SignUpGymOwnerView.as_view(), name='gym-owner-signup'),
    path('gym-owner/login/', LoginGymOwnerView.as_view(), name='gym-owner-login'),
]
