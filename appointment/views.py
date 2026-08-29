from rest_framework import viewsets

from appointment.models import Appointment
from appointment.serizlizers import AppointmentSerializer


class AppointmentView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
