from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from doctors_and_slots_service.models import Doctor
from doctors_and_slots_service.serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filterset_fields = ["id", "specializations"]
