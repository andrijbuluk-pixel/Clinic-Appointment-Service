from django.utils import timezone
from celery import shared_task
from appointment.models import Appointment
from payment.models import Payment


@shared_task
def auto_mark_no_show_appointments():
    expired_appointments = Appointment.objects.filter(
        status="BOOKED",
        doctor_slot__end__lt=timezone.now(),
    )

    for appointment in expired_appointments:
        appointment.status = "NO_SHOW"
        appointment.completed_at = timezone.now()
        appointment.save()
        Payment.objects.create(
            status=Payment.Status.PENDING,
            type=Payment.Type.NO_SHOW_FEE,
            appointment=appointment,
            money_to_pay=300
        )
