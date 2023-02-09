from django.urls import path

from .views import *

urlpatterns = [
    path('trainee-preregister/<int:gym_id>', TraineePreRegistrationView.as_view(), name='trainee-pre-reg-create'),
    path('preregisterlist/', GymPreRegistrationListView.as_view(), name='trainee-pre-reg'),
    # path('TraineePreReg_submit/<int:pk>/', TraineePreRegistrationSubmitView.as_view(), name='trainee-pre-reg-submit'),
]
