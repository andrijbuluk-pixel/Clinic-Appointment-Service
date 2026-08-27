from rest_framework.routers import DefaultRouter

from specializations_service.views import SpecializationViewSet

app_name = 'specializations_service'

router = DefaultRouter()
router.register("specializations", SpecializationViewSet)

urlpatterns = router.urls
