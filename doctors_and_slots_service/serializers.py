from rest_framework import serializers

from doctors_and_slots_service.models import Doctor, DoctorSlot


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "id",
            "first_name",
            "last_name",
            "specializations",
            "price_per_visit"
        )


class DoctorSlotSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = DoctorSlot
        fields = (
            "doctor",
            "start",
            "end"
        )
