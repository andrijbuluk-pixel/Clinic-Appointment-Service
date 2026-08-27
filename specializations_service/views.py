from django.shortcuts import render

from specializations_service.serializers import SpecializationSerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
