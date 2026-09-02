from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and (request.method in permissions.SAFE_METHODS or request.user.is_staff))

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.method in permissions.SAFE_METHODS or request.user.is_staff))


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return request.user.id == obj.patient.id
