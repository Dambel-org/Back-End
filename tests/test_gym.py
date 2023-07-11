from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from account.models import Trainee, GymOwner, Trainer
from gym.models import TraineePreRegistration, Gym, Invitation, GymTrainer, GymTrainee, Province, SportField
from gym.serializers import (
    TraineePreRegistrationSerializer,
    GymTraineeSerializer,
    CreateGymSerializer,
    ProvinceSerializer,
    SportFieldSerializer,
    CreateInviteSerializer,
    InviteSerializer,
    AcceptInviteSerializer,
)

User = get_user_model()
client = APIClient()


def test_trainee_pre_registration_create_view(db):
    gym_owner_user = User.objects.create_user(email='gymowner@example.com', password='testpassword')
    gym_owner = GymOwner.objects.create(user=gym_owner_user)
    gym = Gym.objects.create(name='Test Gym', gym_owner=gym_owner)
    url = reverse('/gym/trainee-pre-registration-create', kwargs={'gym_id': gym.id})
    data = {
        'trainee': {
            'user': {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'johndoe@example.com',
                'password': 'testpassword',
            },
            'height': 170,
            'weight': 70,
        }
    }
    client.force_authenticate(user=gym_owner_user)
    response = client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert TraineePreRegistration.objects.count() == 1


def test_trainee_pre_registration_list_view(db):
    gym_owner_user = User.objects.create_user(email='gymowner@example.com', password='testpassword')
    gym_owner = GymOwner.objects.create(user=gym_owner_user)
    gym = Gym.objects.create(name='Test Gym', gym_owner=gym_owner)
    TraineePreRegistration.objects.create(gym=gym, trainee=Trainee.objects.create())
    url = reverse('/gym/trainee-pre-registration-list')
    client.force_authenticate(user=gym_owner)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_submit_trainee_pre_registration_view(db):
    gym_owner_user = User.objects.create_user(email='gymowner@example.com', password='testpassword')
    gym_owner = GymOwner.objects.create(user=gym_owner_user)
    gym = Gym.objects.create(name='Test Gym', gym_owner=gym_owner)
    trainee = Trainee.objects.create()
    TraineePreRegistration.objects.create(gym=gym, trainee=trainee)
    url = reverse('/gym/submit-trainee-pre-registration', kwargs={'gym_id': gym.id, 'trainee_id': trainee.id})
    data = {}
    client.force_authenticate(user=gym_owner)
    response = client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert GymTrainee.objects.count() == 1


def test_gym_create_view(db):
    client = Client()
    gym_owner_user = User.objects.create_user(email='gymowner@example.com', password='testpassword')
    gym_owner = GymOwner.objects.create(user=gym_owner_user)
    url = reverse('gym-create')
    data = {
        'name': 'Test Gym',
        'logo_image': 'test_image.png',
        'background_image': 'background_image.png',
        'description': 'Test description',
        'sport_field': [1, 2],
        'city_id': 1,
        'contacts': 'Test contacts',
        'map_location': {
            'latitude': 12.345678,
            'longitude': 98.765432,
            'address': 'Test address',
        }
    }
    client.login(email='gymowner@example.com', password='testpassword')
    response = client.post(url, data=data, format='json')


def test_gym_list_view(db):
    gym_owner_user = User.objects.create_user(email='gymowner@example.com', password='testpassword')
    gym_owner = GymOwner.objects.create(user=gym_owner_user)
    Gym.objects.create(name='Test Gym 1', gym_owner=gym_owner)
    Gym.objects.create(name='Test Gym 2', gym_owner=gym_owner)
    url = reverse('gym-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_gym_detail_view(db):
    gym_owner_user = User.objects.create_user(email='gymowner@example.com', password='testpassword')
    gym_owner = GymOwner.objects.create(user=gym_owner_user)
    gym = Gym.objects.create(name='Test Gym', gym_owner=gym_owner)
    url = reverse('gym-detail', kwargs={'gym_id': gym.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_province_list_view(db):
    Province.objects.create(name='Province 1')
    Province.objects.create(name='Province 2')
    url = reverse('province-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_province_detail_view(db):
    province = Province.objects.create(name='Province 1')
    url = reverse('province-detail', kwargs={'province_id': province.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_sport_field_list_view(db):
    SportField.objects.create(name='Sport Field 1')
    SportField.objects.create(name='Sport Field 2')
    url = reverse('sportfield-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_create_invite_trainers_view(db):
    gym_owner_user = User.objects.create_user(email='gymowner@example.com', password='testpassword')
    gym_owner = GymOwner.objects.create(user=gym_owner_user)
    gym = Gym.objects.create(name='Test Gym', gym_owner=gym_owner)
    trainer = Trainer.objects.create()
    url = reverse('create-invite-trainers')
    data = {
        'gym_id': gym.id,
        'trainer_id': trainer.id,
    }
    client.force_authenticate(user=gym_owner)
    response = client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Invitation.objects.count() == 1


def test_invitation_view_list(db):
    trainer = Trainer.objects.create(
        user=User.objects.create_user(email='trainer@example.com', password='testpassword'))
    Invitation.objects.create(gym=Gym.objects.create(), trainer=trainer)
    url = reverse('invitation-list')
    client.force_authenticate(user=trainer.user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_accept_invitation_by_trainer_view(db):
    trainer = Trainer.objects.create(
        user=User.objects.create_user(email='trainer@example.com', password='testpassword'))
    gym = Gym.objects.create()
    Invitation.objects.create(gym=gym, trainer=trainer)
    url = reverse('accept-invitation')
    data = {'gym_id': gym.id}
    client.force_authenticate(user=trainer.user)
    response = client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert GymTrainer.objects.count() == 1