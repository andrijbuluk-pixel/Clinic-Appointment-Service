from django.urls import path, include
from rest_framework.routers import DefaultRouter

from doctors_and_slots_service.views import DoctorViewSet, DoctorSlotsCreateAPIView

app_name = "doctors_and_slots_service"

router = DefaultRouter()

router.register("", DoctorViewSet, basename="doctors")

urlpatterns = [
    path('', include(router.urls)),
    path("<int:pk>/slots/", DoctorSlotsCreateAPIView.as_view(), name="doctor-slots")
]
