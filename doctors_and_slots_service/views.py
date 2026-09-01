from rest_framework import viewsets, generics, status, mixins
from rest_framework.response import Response
from datetime import datetime, timedelta
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from doctors_and_slots_service.models import Doctor, DoctorSlot
from doctors_and_slots_service.serializers import DoctorSerializer, DoctorSlotSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filterset_fields = ["id", "specializations"]


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="from",
            required=False,
            type=OpenApiTypes.DATETIME,
        ),
        OpenApiParameter(
            name="to",
            required=False,
            type=OpenApiTypes.DATETIME,
        ),
        OpenApiParameter(
            name="available_only",
            required=False,
            type=OpenApiTypes.BOOL,
        )
    ]
)
class DoctorSlotsCreateAPIView(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    queryset = DoctorSlot.objects.all()
    serializer_class = DoctorSlotSerializer

    def get_queryset(self):
        doctor_id = self.kwargs.get("pk")
        queryset = DoctorSlot.objects.filter(doctor_id=doctor_id)

        from_dt = self.request.query_params.get("from")
        to_dt = self.request.query_params.get("to")
        availability = self.request.query_params.get("available_only")

        if from_dt:
            queryset = queryset.filter(start__gte=from_dt)

        if to_dt:
            queryset = queryset.filter(end__lte=to_dt)

        if str(availability).lower() == "true":
            queryset = queryset.exclude(appointment__status="BOOKED")

        return queryset


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