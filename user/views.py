from rest_framework import viewsets

from user.models import User
from user.serizlizers import UserSerializer


class CreateUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
