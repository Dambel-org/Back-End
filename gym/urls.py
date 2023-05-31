from django.urls import path

from .views import *

urlpatterns = [

    path('trainee-preregister/<int:gym_id>', TraineePreRegistrationCreateView.as_view(), name='trainee-pre-reg-create'),
    path('preregisters/<int:gym_id>', TraineePreRegistrationListView.as_view(), name='trainee-pre-reg-list'),
    path('submit-trianee-preregister/<int:gym_id>/<int:trainee_id>/', SubmitTraineePreRegistrationView.as_view(),
         name='trainee-pre-reg-submit'),
    path('list/', GymListView.as_view(), name='gym-list'),

    path('detail/<int:gym_id>/', GymDetailView.as_view(), name='gym-detail'),
    path('create/', GymCreateView.as_view(), name='gym-create'),
    path('provinces/', ProvinceListView.as_view(), name='province-list'),
    path('provinces/<int:province_id>/', ProvinceDetailView.as_view(), name='province-detail'),
    path('invitations/<int:trainer_id>/', InvitationViewList.as_view(), name="invitation-list"),
    path('invite-trainers/', CreateInviteTrainersView.as_view(), name='invite-trainer-create'),
    #trainers_id & gym_id
    path('accept-invite/<int:gym_id>/<int:trainee_id>/', AcceptInvitationByTrainer.as_view(), name='gym-trainer-create')
]
