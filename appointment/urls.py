from django.urls import path, include
from rest_framework.routers import DefaultRouter

from appointment.views import AppointmentView


app_name = 'appointment'

router = DefaultRouter()

router.register(r"", AppointmentView, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
]
