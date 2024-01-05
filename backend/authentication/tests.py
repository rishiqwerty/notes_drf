from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class LoginApiTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_login_successful(self):
        url = "/api/auth/login/"

        data = {"username": self.username, "password": self.password}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)

    def test_login_unsuccessful(self):
        url = "/api/auth/login/"

        data = {"username": self.username, "password": "wrongpassword"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 401)


class SignupApiTests(APITestCase):
    def test_signup_successful(self):
        url = "/api/auth/signup/"

        data = {
            "email": "newuser",
            "first_name": "test",
            "last_name": "user",
            "password": "test",
            "password_confirm": "test",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_signup_unsuccessful(self):
        url = "/api/auth/signup/"

        data = {
            "password": "newpassword",
            "email": "newuser@example.com",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username="newuser").exists())
