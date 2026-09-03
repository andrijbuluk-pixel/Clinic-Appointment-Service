from datetime import timedelta
from django.utils import timezone
from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from doctors_and_slots_service.models import Doctor
from specializations_service.models import Specialization
from user.models import User


class DoctorsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="user@gmail.com",
            first_name="test_user",
            last_name="test_user",
            password="test_password"
        )

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

        self.doctor = Doctor.objects.create(
            first_name='test_doctor',
            last_name='test_doctor',
            price_per_visit=500,
        )
        self.doctor.specializations.add(self.specializations)


    def test_create_doctor(self):
        self.client.force_authenticate(user=self.user_admin)

        data = {
            "first_name": "First",
            "last_name": "Last",
            "specializations": self.specializations.id,
            "price_per_visit": 500,
        }

        response = self.client.post(reverse("doctors_and_slots_service:doctors-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_doctor(self):
        self.client.force_authenticate(user=self.user_admin)

        response = self.client.patch(reverse(
            "doctors_and_slots_service:doctors-detail", args=[self.doctor.id]),
        data={
            "first_name": "First",
            "last_name": "Last",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_doctor(self):
        self.client.force_authenticate(user=self.user_admin)

        response = self.client.delete(reverse(
            "doctors_and_slots_service:doctors-detail", args=[self.doctor.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_doctor_slot(self):
        self.client.force_authenticate(user=self.user_admin)

        data = {
            "doctor": self.doctor.id,
            "start": "2026-09-04 09:00:00",
            "end": "2026-09-04 15:00:00"
        }

        response = self.client.post(
            reverse("doctors_and_slots_service:doctor-slots", args=[self.doctor.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_doctor_slot(self):
        self.client.force_authenticate(user=self.user_admin)

        response = self.client.delete(reverse(
            "doctors_and_slots_service:doctor-slots",
            args=[self.doctor.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_doctor_not_authorized(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(reverse(
            "doctors_and_slots_service:doctors-detail", args=[self.doctor.id]),
        data={
            "first_name": "First",
            "last_name": "Last",
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
