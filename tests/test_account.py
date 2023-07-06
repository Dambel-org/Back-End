from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import *


class BaseUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
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
        self.response = self.client.post(
            reverse('gymowner-signup'),
            self.user_data,
            format='json'
        )

    def test_api_can_create_a_user(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class GymOwnerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
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
        self.signup_gymowner_url = reverse('gymowner-signup')

    def test_api_can_create_a_gym_owner(self):
        response = self.client.post(self.signup_gymowner_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BaseUser.objects.count(), 1)

    def test_api_returns_bad_request_on_missing_required_fields(self):
        user_data = {
            'user': {
                'email': 'test@test.com',
                'last_name': 'test',
                'age': 20,
                'password': 'test',
            },
            'license_number': '123456789',
        }

        response = self.client.post(self.signup_gymowner_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_returns_bad_request_on_existing_email(self):
        BaseUser.objects.create_user(
            email='test@test.com',
            first_name='nobody',
            last_name='user',
            age=30,
            password='nobodypass',
        )

        response = self.client.post(self.signup_gymowner_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_returns_bad_request_on_invalid_data(self):
        user_data = {
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'age': 'twenty',
            'password': 'test',
            'license_number': '123456789',
            'phone_number': '09123456789',
        }

        response = self.client.post(self.signup_gymowner_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SignUpTraineeViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
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
        self.signup_trainee_url = reverse('trainee-signup')

    def test_signup_trainee_with_valid_data(self):
        response = self.client.post(self.signup_trainee_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_trainee_with_missing_required_fields(self):
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
        }

        response = self.client.post(self.signup_trainee_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_trainee_with_existing_email(self):
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

        response = self.client.post(self.signup_trainee_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_trainee_with_invalid_data(self):
        data = {
            'first_name': 'test',
            'last_name': 'test',
            'age': 'twenty-five',
            'email': 'test@test.com',
            'height': 180.5,
            'weight': 75.0
        }

        response = self.client.post(self.signup_trainee_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SignUpTrainerViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
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
        self.signup_trainer_url = reverse('trainer-signup')

    def test_signup_trainer_with_valid_data(self):
        response = self.client.post(self.signup_trainer_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_trainer_with_missing_required_fields(self):
        data = {
            'user': {
                'email': 'test@test.com',
                'first_name': 'test',
                'last_name': 'test',
                'age': 20,
                'password': 'test',
            },
            'phone_number': {
            }
        }

        response = self.client.post(self.signup_trainer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_trainer_with_existing_email(self):
        BaseUser.objects.create_user(
            email='test@test.com',
            first_name='nobody',
            last_name='user',
            age=30,
            password='nobodypass',
        )

        response = self.client.post(self.signup_trainer_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_trainer_with_invalid_data(self):
        data = {
            'user': {
                'email': 'test@test.com',
                'first_name': 'test',
                'last_name': 'test',
                'age': 'twenty',
                'password': 'test',
            }
        }

        response = self.client.post(self.signup_trainer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = BaseUser.objects.create_user(
            email='test@test.com',
            first_name='test',
            last_name='test',
            age=30,
            password='testpassword'
        )
        self.login_url = reverse('login')

    def test_login_view_with_invalid_credentials(self):
        data = {
            'email': 'test@test.com',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def login_view_with_role(self, role):
        if role == 'GymOwner':
            GymOwner.objects.create(user=self.user, license_number='123456789')
        elif role == 'Trainee':
            Trainee.objects.create(user=self.user, height=180, weight=75)
        elif role == 'Trainer':
            trainer_phone_number = PhoneNumber.objects.create(number='09123456789')
            Trainer.objects.create(user=self.user, phone_number=trainer_phone_number)

        user_data = {
            'email': 'test@test.com',
            'password': 'testpassword'
        }

        response = self.client.post(self.login_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['role'], role)

    def test_login_view_with_gym_owner_role(self):
        self.login_view_with_role('GymOwner')

    def test_login_view_with_trainee_role(self):
        self.login_view_with_role('Trainee')

    def test_login_view_with_trainer_role(self):
        self.login_view_with_role('Trainer')

    def test_refresh_token_valid(self):
        user_data = {
            'email': 'test@test.com',
            'password': 'testpassword',
        }

        response = self.client.post(self.login_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_token = response.data.get('refresh', None)
        self.assertIsNotNone(refresh_token)

        refresh = RefreshToken(refresh_token)
        current_time = datetime.utcnow()
        expiration_time = refresh.payload['exp']
        self.assertGreater(expiration_time, current_time.timestamp())
