from django.urls import path, include
from rest_framework.routers import DefaultRouter

from specializations_service.views import SpecializationViewSet

app_name = "specializations_service"

router = DefaultRouter()

router.register("", SpecializationViewSet, basename="specializations")

urlpatterns = [
    path("", include(router.urls)),

]
