from django.urls import path

from .views import *

urlpatterns = [
    path('my/', UserGymView.as_view(), name='my-gym'),
    path('my/plans/', TraineePlanView.as_view(), name='trainee-plans'),

    # path('trainee-preregister/<int:gym_id>', TraineePreRegistrationCreateView.as_view(), name='trainee-pre-reg-create'),
    # path('preregisters/<int:gym_id>', TraineePreRegistrationListView.as_view(), name='trainee-pre-reg-list'),
    # path('submit-trianee-preregister/<int:gym_id>/<int:trainee_id>/', SubmitTraineePreRegistrationView.as_view(),
    #      name='trainee-pre-reg-submit'),

    path('list/', GymListView.as_view(), name='gym-list'),
    path('detail/<int:gym_id>/', GymDetailView.as_view(), name='gym-detail'),
    path('create/', GymCreateView.as_view(), name='gym-create'),

    path('provinces/', ProvinceListView.as_view(), name='province-list'),
    path('provinces/<int:province_id>/', ProvinceDetailView.as_view(), name='province-detail'),

    path('plan/create/<int:gym_id>', CreatePlanView.as_view(), name='plan-list'),

    path('invitations/', InvitationViewList.as_view(), name="invitation-list"),
    path('invite-trainers/', CreateInviteTrainersView.as_view(), name='invite-trainer-create'),
    path('accept-invite/', AcceptInvitationByTrainer.as_view(), name='gym-trainer-create'),

    path('requests/', RequestViewList.as_view(), name="invitation-list"),
    path('request-trainee/', CreateRequestTraineeView.as_view(), name='invite-trainee-create'),
    path('accept-request/', AcceptRequestByGymOwner.as_view(), name='accept-request'),

    path('comment/create/', CommentCreateView.as_view(), name='add-comment'),

]
