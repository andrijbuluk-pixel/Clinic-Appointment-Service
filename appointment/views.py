from datetime import timedelta
from django.utils import timezone

from rest_framework import viewsets, status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from appointment.models import Appointment
from payment.models import Payment
from appointment.serizlizers import AppointmentSerializer

class AppointmentView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = [
        "patient",
        "status",
        "doctor_slot__doctor",
        "doctor_slot"
    ]

    @action(methods=["post"], detail=True)
    def cancel(self, request, pk=None):
        appointment = self.get_object()

        if appointment.doctor_slot.start - timedelta(hours=12) < timezone.now():
            Payment.objects.create(
                status=Payment.Status.PENDING,
                type=Payment.Type.CANCELLATION_FEE,
                appointment=appointment,
                money_to_pay=300
            )

        appointment.status = "Canceled"
        appointment.save()
        return Response(f"Appointment {pk} has been <Canceled>", status=status.HTTP_202_ACCEPTED)

    @action(methods=["post"], detail=True)
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = "Completed"
        appointment.completed_at = timezone.now()
        appointment.save()
        return Response(f"Appointment {pk} has been <Completed>", status=status.HTTP_202_ACCEPTED)

    @action(methods=["post"], detail=True)
    def no_show(self, request, pk=None):
        appointment = self.get_object()
        user = request.user

        if not (user.is_superuser or user.is_staff):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if appointment.doctor_slot.start + timedelta(minutes=40) < timezone.now() and appointment.status == "Booked":
            Payment.objects.create(
                status=Payment.Status.PENDING,
                type=Payment.Type.CANCELLATION_FEE,
                appointment=appointment,
                money_to_pay=300
            )

        appointment.status = "No show"
        appointment.save()
        return Response(f"Appointment {pk} has been <No show>", status=status.HTTP_202_ACCEPTED)
