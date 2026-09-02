from rest_framework import viewsets

from specializations_service.models import Specialization
from specializations_service.serializers import SpecializationSerializers
from clinic_service.permissions import IsAdminOrReadOnly

class SpecializationViewSet(viewsets.ModelViewSet):
    serializer_class = SpecializationSerializers
    queryset = Specialization.objects.all()
    permission_classes = [IsAdminOrReadOnly]
