from rest_framework import viewsets

from specializations_service.models import Specialization
from specializations_service.serializers import SpecializationSerializers


class SpecializationViewSet(viewsets.ModelViewSet):
    serializer_class = SpecializationSerializers
    queryset = Specialization.objects.all()
