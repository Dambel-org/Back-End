from django.urls import path

from .views import *

urlpatterns = [
    path('trainee-preregister/<int:gym_id>', TraineePreRegistrationCreateView.as_view(), name='trainee-pre-reg-create'),
    path('preregisters/<int:gym_id>', TraineePreRegistrationListView.as_view(), name='trainee-pre-reg-list'),
    path('submit-trianee-preregister/<int:gym_id>/<int:trainee_id>/', SubmitTraineePreRegistrationView.as_view(),
         name='trainee-pre-reg-submit'),
]
