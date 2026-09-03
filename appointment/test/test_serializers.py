from datetime import datetime
from django.utils import timezone

from django.urls import reverse
from datetime import timedelta
from rest_framework import status
from django.test import override_settings
from rest_framework.test import APITestCase, APIClient

from appointment.models import Appointment
from doctors_and_slots_service.models import Doctor, DoctorSlot
from specializations_service.models import Specialization
from user.models import User


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class AppointmentTest(APITestCase):
    time_continues_1 = datetime(2026, 9, 4, 10, 0, 0)
    time_continues_2 = datetime(2026, 9, 4, 10, 30, 0)

    time_passed_1 = datetime(2026, 9, 2, 10, 0, 0)
    time_passed_2 = datetime(2026, 9, 2, 10, 30, 0)

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@gmail.com",
            first_name="test_user",
            last_name="test_user",
            password="test_password"
        )

        self.user_2 = User.objects.create_user(
            email="user2@gmail.com",
            first_name="test_user2",
            last_name="test_user2",
            password="test_password2"
        )

        self.user_admin = User.objects.create_superuser(
            email="admin@gmail.com",
            first_name="admin_test",
            last_name="admin_test",
            password="admin_test",
            is_staff=True,
        )

        self.specializations = Specialization.objects.create(
            name="test_specialization",
            code="test_specialization",
            description="test_specialization",
        )

        self.doctor = Doctor.objects.create(
            first_name="test_doctor",
            last_name="test_doctor",
            price_per_visit=600
        )
        self.doctor.specializations.add(self.specializations)

        # You can still make an appointment 1
        self.doctor_slot_continues_1 = DoctorSlot.objects.create(
            doctor=self.doctor,
            start=self.time_continues_1,
            end=self.time_continues_2
        )

        # You can still make an appointment 2
        self.doctor_slot_continues_2 = DoctorSlot.objects.create(
            doctor=self.doctor,
            start=self.time_continues_1,
            end=self.time_continues_2
        )

        # The time has already passed
        self.doctor_slot_passed = DoctorSlot.objects.create(
            doctor=self.doctor,
            start=self.time_passed_1,
            end=self.time_passed_2
        )

        self.appointment = Appointment.objects.create(
            doctor_slot=self.doctor_slot_continues_1,
            patient=self.user,
            status="Booked",
            booked_at=timezone.now(),
            completed_at=timezone.now() + timedelta(minutes=30),
            price=1000
        )

    def test_create_appointment(self):
        self.client.force_authenticate(self.user)

        data = {
            "doctor_slot": self.doctor_slot_continues_2.id,
            "patient": self.user.id,
            "status": "BOOKED",
            "booked_at": timezone.now(),
            "completed_at": timezone.now() + timedelta(minutes=30),
            "price": 1000
        }

        response = self.client.post(reverse("appointment:appointment-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_status_update_canceled(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(reverse(
            "appointment:appointment-cancel",
            args=[self.appointment.id]),
            {"status": "Canceled"})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_status_update_completed(self):
        self.client.force_authenticate(self.user_admin)

        response = self.client.post(reverse(
            "appointment:appointment-complete",
            args=[self.appointment.id]),
            {"status": "Completed"})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_status_update_no_show(self):
        self.client.force_authenticate(self.user_admin)

        response = self.client.post(reverse(
            "appointment:appointment-no-show",
            args=[self.appointment.id]),
            {"status": "No show"})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
