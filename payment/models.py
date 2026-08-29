from django.db import models

from appointment.models import Appointment


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        EXPIRED = "EXPIRED", "Expired"

    class Type(models.TextChoices):
        CONSULTATION = "CONSULTATION", "Consulation"
        CANCELLATION_FEE = "CANCELLATION_FEE", "Cancellation_fee"
        NO_SHOW_FEE = "NO_SHOW_FEE", "no_show_fee"


    status = models.CharField(choices=Status.choices, default=Status.PENDING, max_length=50)
    type = models.CharField(choices=Type.choices, max_length=50)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="payments")
    session_url = models.CharField(blank=True, null=True, max_length=1000)
    session_id = models.CharField(blank=True, null=True, max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id} for Appointment {self.appointment.id} - {self.status} "