from django.urls import path

from .views import *

urlpatterns = [
    path('TraineePreReg/', TraineePreRegisterCreateView.as_view(), name='trainee-pre-reg-create'),
    path('TraineePreReg/<int:pk>/', TraineePreRegistrationView.as_view(), name='trainee-pre-reg'),
    path('TraineePreReg_submit/<int:pk>/', TraineePreRegistrationSubmitView.as_view(), name='trainee-pre-reg-submit'),
]