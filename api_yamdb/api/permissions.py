from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для администратора или чтение для всех"""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class OwnerOrAdmins(permissions.BasePermission):
    """Разрешение только для администратора или владельца"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin
            or request.user.is_superuser
        )


class AuthorAndStaffOrReadOnly(BasePermission):
    """Разрешение для модератора, владельца или чтение авторизированных"""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (obj.author == request.user or request.user.is_moderator)
        )
