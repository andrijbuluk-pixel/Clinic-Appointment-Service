from django.db import models

from specializations_service.models import Specialization


class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    specializations = models.ManyToManyField(Specialization)
    price_per_visit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DoctorSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start = models.DateTimeField ()
    end = models.DateTimeField ()
