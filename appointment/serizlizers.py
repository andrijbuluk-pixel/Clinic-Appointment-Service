from rest_framework import serializers

from appointment.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            "id",
            "doctor_slot_id",
            "patient_id",
            "status",
            "booked_at",
            "completed_at",
            "price"
        )

        read_only_fields = ("id",)
