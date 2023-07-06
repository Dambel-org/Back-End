from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import *
from .serializers import *


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
                'conf_password': 'test'
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
            'conf_password': 'test',
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

