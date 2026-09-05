from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from specializations_service.models import Specialization
from user.models import User


class SpecializationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_admin = User.objects.create_superuser(
            email="admin@gmail.com",
            first_name="admin_test",
            last_name="admin_test",
            password="admin_test",
            is_staff=True,
        )

        self.specializations = Specialization.objects.create(
            name="test_spec_1",
            code="test_spec_1",
            description="test_specialization",
        )


    def test_create_specialization(self):
        self.client.force_authenticate(user=self.user_admin)

        data = {
            "name": "test_spec_2",
            "code": "test_spec_2",
            "description": "test_specialization",
        }

        response = self.client.post(reverse("specializations_service:specializations-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_specialization(self):
        self.client.force_authenticate(user=self.user_admin)

        response = self.client.patch(reverse(
            "specializations_service:specializations-detail",
            args=[self.specializations.id]),
            data={"description": "test_specialization - test_specialization - test_specialization"},
        )
        print(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_specialization(self):
        self.client.force_authenticate(user=self.user_admin)

        response = self.client.delete(reverse(
            "specializations_service:specializations-detail",
            args=[self.specializations.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
