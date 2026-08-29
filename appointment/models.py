from django.db import models

from specializations_service.models import Specialization
from doctors_and_slots_service.models import Doctor
from user.models import User


class Appointment(models.Model):
    STATUS_CHOICES = (
        ("BOOKED", "Booked"),
        ("COMPLETED", "Completed"),
        ("CANCELED", "Canceled"),
        ("NO_SHOW", "No show"),
    )

    doctor_slot = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, blank=True, null=True, max_length=50)
    booked_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
