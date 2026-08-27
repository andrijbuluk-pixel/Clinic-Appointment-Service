from rest_framework import serializers

from doctors_and_slots_service.models import Doctor


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