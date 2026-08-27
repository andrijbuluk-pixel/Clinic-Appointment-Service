from rest_framework import serializers
from specializations_service.models import Specialization


class SpecializationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ("name", "code", "description")
