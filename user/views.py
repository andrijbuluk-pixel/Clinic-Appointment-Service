from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from user.models import User
from user.serizlizers import UserSerializer


class CreateUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["get", "put", "patch"])
    def me(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        kwargs = {'partial': True} if request.method == 'PATCH' else {}
        serializer = self.get_serializer(user, data=request.data, **kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

