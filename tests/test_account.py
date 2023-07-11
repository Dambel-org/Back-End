from datetime import datetime

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import *

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def signup_gymowner_url():
    return reverse('gymowner-signup')


@pytest.fixture
def signup_trainee_url():
    return reverse('trainee-signup')


@pytest.fixture
def signup_trainer_url():
    return reverse('trainer-signup')


@pytest.fixture
def login_url():
    return reverse('login')


@pytest.mark.django_db
def test_api_can_create_a_gym_owner(api_client, signup_gymowner_url):
    data = {
        'user': {
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'age': 20,
            'password': 'test',
            'conf_password': 'test'
        },
        'license_number': '123456789',
        'phone_number': '09123456789',
    }
    response = api_client.post(signup_gymowner_url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_api_returns_bad_request_on_missing_required_fields(api_client, signup_gymowner_url):
    data = {
        'user': {
            'email': 'test@test.com',
            'last_name': 'test',
            'age': 20,
            'password': 'test',
        },
        'license_number': '123456789',
    }

    response = api_client.post(signup_gymowner_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_api_returns_bad_request_on_existing_email(api_client, signup_gymowner_url):
    data = {
        'user': {
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'age': 20,
            'password': 'test',
            'conf_password': 'test'
        },
        'license_number': '123456789',
        'phone_number': '09123456789',
    }
    BaseUser.objects.create_user(
        email='test@test.com',
        first_name='nobody',
        last_name='user',
        age=30,
        password='nobodypass',
    )

    response = api_client.post(signup_gymowner_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_api_returns_bad_request_on_invalid_data(api_client, signup_gymowner_url):
    data = {
        'email': 'test@test.com',
        'first_name': 'test',
        'last_name': 'test',
        'age': 'twenty',
        'password': 'test',
        'license_number': '123456789',
        'phone_number': '09123456789',
    }

    response = api_client.post(signup_gymowner_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_trainee_with_valid_data(api_client, signup_trainee_url):
    data = {
        'user': {
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'age': 20,
            'password': 'test',
            'conf_password': 'test'
        },
        'height': 180,
        'weight': 80,
        'phone_number': '09123456789',
    }
    response = api_client.post(signup_trainee_url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_signup_trainee_with_missing_required_fields(api_client, signup_trainee_url):
    data = {
        'user': {
            'email': 'test@test.com',
            'first_name': 'test',
            'age': 20,
            'password': 'test',
            'conf_password': 'test'
        },
        'height': 180,
    }

    response = api_client.post(signup_trainee_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_trainee_with_existing_email(api_client, signup_trainee_url):
    BaseUser.objects.create_user(
        first_name='hamed',
        last_name='khosravi',
        age=21,
        email='test@test.com',
        password='password'
    )

    data = {
        'first_name': 'test',
        'last_name': 'test',
        'age': 25,
        'email': 'test@test.com',
        'height': 180.5,
        'weight': 75.0
    }

    response = api_client.post(signup_trainee_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_trainee_with_invalid_data(api_client, signup_trainee_url):
    data = {
        'first_name': 'test',
        'last_name': 'test',
        'age': 'twenty-five',
        'email': 'test@test.com',
        'height': 180.5,
        'weight': 75.0
    }

    response = api_client.post(signup_trainee_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_trainer_with_valid_data(api_client, signup_trainer_url):
    data = {
        'user': {
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'age': 20,
            'password': 'test',
        },
        'phone_number': {
            'number': '09123456789',
        }
    }
    response = api_client.post(signup_trainer_url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_signup_trainer_with_missing_required_fields(api_client, signup_trainer_url):
    data = {
        'user': {
            'email': 'test@test.com',
            'first_name': 'test',
            'age': 20,
            'password': 'test',
        },

    }

    response = api_client.post(signup_trainer_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_trainer_with_existing_email(api_client, signup_trainer_url):
    data = {
        'user': {
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'age': 20,
            'password': 'test',
        },
        'phone_number': {
            'number': '09123456789',
        }
    }
    BaseUser.objects.create_user(
        email='test@test.com',
        first_name='nobody',
        last_name='user',
        age=30,
        password='nobodypass',
    )

    response = api_client.post(signup_trainer_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_trainer_with_invalid_data(api_client, signup_trainer_url):
    data = {
        'first_name': 'test',
        'last_name': 'test',
        'age': 'twenty-five',
        'email': 'test@test.com',
    }

    response = api_client.post(signup_trainer_url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_login_view_with_invalid_credentials(api_client, login_url):
    BaseUser.objects.create_user(
        email='test@test.com',
        first_name='test',
        last_name='test',
        age=30,
        password='testpassword'
    )
    data = {
        'email': 'test@test.com',
        'password': 'wrongpassword'
    }

    response = api_client.post(login_url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def login_view_with_role(role, api_client, login_url):
    user = BaseUser.objects.create_user(
        email='test@test.com',
        first_name='test',
        last_name='test',
        age=30,
        password='testpassword'
    )

    if role == 'GymOwner':
        GymOwner.objects.create(user=user, license_number='123456789')
    elif role == 'Trainee':
        Trainee.objects.create(user=user, height=180, weight=75)
    elif role == 'Trainer':
        Trainer.objects.create(user=user)

    data = {
        'email': 'test@test.com',
        'password': 'testpassword'
    }

    response = api_client.post(login_url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert response.data['role'] == role


@pytest.mark.django_db
def test_login_view_with_gym_owner_role(api_client, login_url):
    login_view_with_role('GymOwner', api_client, login_url)


@pytest.mark.django_db
def test_login_view_with_trainee_role(api_client, login_url):
    login_view_with_role('Trainee', api_client, login_url,)


@pytest.mark.django_db
def test_login_view_with_trainer_role(api_client, login_url):
    login_view_with_role('Trainer', api_client, login_url)


@pytest.mark.django_db
def test_refresh_token_valid(api_client, login_url):
    BaseUser.objects.create_user(
        email='test@test.com',
        first_name='test',
        last_name='test',
        age=30,
        password='testpassword'
    )
    data = {
        'email': 'test@test.com',
        'password': 'testpassword',
    }

    response = api_client.post(login_url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

    refresh_token = response.data.get('refresh', None)
    assert refresh_token is not None

    refresh = RefreshToken(refresh_token)
    current_time = datetime.utcnow()
    expiration_time = refresh.payload['exp']
    assert expiration_time > current_time.timestamp()
