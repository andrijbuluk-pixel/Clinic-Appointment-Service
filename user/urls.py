from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import CreateUserView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'user'

router = DefaultRouter()

router.register("", CreateUserView, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]

