from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from user.models import User


class UserTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_admin = User.objects.create_superuser(
            email="admin@gmail.com",
            first_name="admin_test",
            last_name="admin_test",
            password="admin_test",
            is_staff=True,
        )

        self.user = User.objects.create_user(
            email="user@gmail.com",
            first_name="test_user",
            last_name="test_user",
            password="test_password"
        )

    def test_create_user(self):

        data = {
            "email": "user@test.com",
            "first_name": "First",
            "last_name": "Last",
            "password": "password"
        }

        response = self.client.post(reverse("user:user-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse("user:user-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "email": "user@test.com",
            "first_name": "First",
            "last_name": "Last",
            "password": "password",
        }
        response = self.client.patch(reverse("user:user-me"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated_user(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse("user:user-me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
