from datetime import timedelta
from django.utils import timezone

from rest_framework import viewsets, status, mixins

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from appointment.models import Appointment
from payment.models import Payment
from appointment.serizlizers import AppointmentSerializer
from appointment.tasks import auto_message_appointments
from payment.stripe_helper import create_stripe_session
from clinic_service.permissions import IsOwnerOrAdmin


class AppointmentView(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsOwnerOrAdmin]

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = [
        "patient",
        "status",
        "doctor_slot__doctor",
        "doctor_slot"
    ]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        appointment = serializer.save()
        massage_tl = (
            f"New booking!\n"
            f"Doctor: {appointment.doctor_slot.doctor.first_name} - {appointment.doctor_slot.doctor.last_name}\n"
            f"Appointment: #{appointment.id} is <BOOKED>\n"
            f"Beginning : {appointment.doctor_slot.start}\n"
        )
        auto_message_appointments.delay(massage_tl)

    @action(methods=["post"], detail=True)
    def cancel(self, request, pk=None):
        appointment = self.get_object()

        if appointment.doctor_slot.start - timedelta(hours=12) < timezone.now():
            session = create_stripe_session(request, 300, "Cancellation Fee")

            Payment.objects.create(
                status=Payment.Status.PENDING,
                type=Payment.Type.CANCELLATION_FEE,
                appointment=appointment,
                session_id=session.id,
                session_url=session.url,
                money_to_pay=300
            )

        appointment.completed_at = timezone.now()
        appointment.status = "Canceled"
        appointment.save()

        massage_tl = (
            f"{appointment.doctor_slot.doctor.first_name} - {appointment.doctor_slot.doctor.last_name}\n"
            f"This appointment #{appointment.id} has been <Canceled>"
        )
        auto_message_appointments.delay(massage_tl)

        return Response(f"Appointment {pk} has been <Canceled>", status=status.HTTP_202_ACCEPTED)

    @action(methods=["post"], detail=True)
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = "Completed"
        appointment.completed_at = timezone.now()
        appointment.save()

        massage_tl = (
            f"{appointment.doctor_slot.doctor.first_name} - {appointment.doctor_slot.doctor.last_name}\n"
            f"This appointment #{appointment.id} has been <Completed>"
        )
        auto_message_appointments.delay(massage_tl)

        return Response(f"Appointment {pk} has been <Completed>", status=status.HTTP_202_ACCEPTED)

    @action(methods=["post"], detail=True)
    def no_show(self, request, pk=None):
        appointment = self.get_object()
        user = request.user

        if not (user.is_superuser or user.is_staff):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if appointment.doctor_slot.start + timedelta(minutes=40) < timezone.now() and appointment.status == "Booked":
            session = create_stripe_session(request, 300, "No Show")

            Payment.objects.create(
                status=Payment.Status.PENDING,
                type=Payment.Type.CANCELLATION_FEE,
                appointment=appointment,
                session_id=session.id,
                session_url=session.url,
                money_to_pay=300
            )
        appointment.completed_at = timezone.now()
        appointment.status = "NO_SHOW"
        appointment.save()

        massage_tl = (
            f"{appointment.doctor_slot.doctor.first_name} - {appointment.doctor_slot.doctor.last_name}\n"
            f"This appointment #{appointment.id} has been <No show>"
        )
        auto_message_appointments.delay(massage_tl)

        return Response(f"Appointment {pk} has been <No show>", status=status.HTTP_202_ACCEPTED)
