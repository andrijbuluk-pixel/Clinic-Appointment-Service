from rest_framework import viewsets, generics, status, mixins
from rest_framework.response import Response
from datetime import datetime, timedelta

from doctors_and_slots_service.models import Doctor, DoctorSlot
from doctors_and_slots_service.serializers import DoctorSerializer, DoctorSlotSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filterset_fields = ["id", "specializations"]


class DoctorSlotsCreateAPIView(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    queryset = DoctorSlot.objects.all()
    serializer_class = DoctorSlotSerializer

    def create(self, request, *args, **kwargs):
        slots_list = []

        start_dt = datetime.strptime(request.data.get("start"), "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(request.data.get("end"), "%Y-%m-%d %H:%M:%S")

        while start_dt < end_dt:
            slots_list.append(
                DoctorSlot(
                    doctor_id=self.kwargs.get("pk"),
                    start=start_dt,
                    end=start_dt + timedelta(minutes=30)))
            start_dt = start_dt + timedelta(minutes=30)



        created_slots = DoctorSlot.objects.bulk_create(slots_list)

        return Response(
            {"detail": f"Created {len(created_slots)} slots"}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        doctor_id = self.kwargs.get("pk")
        delete_count = DoctorSlot.objects.filter(doctor_id=doctor_id).delete()

        return Response(
            {"detail": f"Deleted {delete_count} slots"}, status=status.HTTP_204_NO_CONTENT
        )