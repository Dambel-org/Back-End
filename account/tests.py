from django.test import TestCase

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
            'http://127.0.0.1:8000/account/gym-owner/signup/',
            self.user_data,
            format='json'
        )

    def test_api_can_create_a_user(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
