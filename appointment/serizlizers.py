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

    class AppointmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Appointment
            fields = "__all__"  # Або твій список полів

        def validate(self, attrs):
            doctor_slot = attrs.get('doctor_slot')

            existing_appointments = Appointment.objects.filter(doctor_slot=doctor_slot)

            if self.instance:
                existing_appointments = existing_appointments.exclude(pk=self.instance.pk)

            if existing_appointments.exists():
                raise serializers.ValidationError({
                    "doctor_slot": "This appointment already exists"
                })

            return attrs
