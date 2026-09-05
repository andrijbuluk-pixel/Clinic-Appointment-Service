from rest_framework import serializers

from appointment.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            "id",
            "doctor_slot",
            "patient",
            "status",
            "booked_at",
            "completed_at",
            "price"
        )

        read_only_fields = ("id", "completed_at")
