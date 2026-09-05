import stripe
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from appointment.tasks import auto_message_appointments
from payment.models import Payment
from payment.serializers import PaymentSerializer
from clinic_service.permissions import IsOwnerOrAdmin
from rest_framework.permissions import AllowAny


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsOwnerOrAdmin]

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def success(self, request):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response({"error": "session_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        stripe.api_key = settings.STRIPE_API_KEY

        session = stripe.checkout.Session.retrieve(session_id)
        payment = Payment.objects.get(session_id=session_id)

        if session.payment_status == "paid":
            payment.status = Payment.Status.PAID
            payment.save()
            message = (
                f"Payment #{payment.id} successful!\n"
                f"Amount: {payment.money_to_pay} USD\n"
                f"Type: {payment.type}\n"
                f"Appointment #{payment.appointment.id}\n"
            )

            auto_message_appointments.delay(message)

        return Response({"status": "Payment successful!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def cancel(self, request):
        return Response({"message": "Payment canceled!"}, status=status.HTTP_200_OK)
