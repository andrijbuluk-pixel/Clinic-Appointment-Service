import os
import requests

from django.utils import timezone
from celery import shared_task
from appointment.models import Appointment
from payment.models import Payment
from payment.stripe_helper import create_stripe_session


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

        massage_tl = (
            f"{appointment.doctor_slot.doctor.first_name} - {appointment.doctor_slot.doctor.last_name}\n"
            f"This appointment #{appointment.id} has been <No show>"
        )
        auto_message_appointments.delay(massage_tl)

        session = create_stripe_session(
            request=None,
            money_to_pay=300,
            service_name=f"No-show fee for appointment #{appointment.id}"
        )

        Payment.objects.create(
            status=Payment.Status.PENDING,
            type=Payment.Type.NO_SHOW_FEE,
            appointment=appointment,
            session_id=session.id,
            session_url=session.url,
            money_to_pay=300
        )


@shared_task
def auto_message_appointments(message: str) -> None:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=data)
    print(response.json())
