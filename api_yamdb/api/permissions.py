from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == User.UserRole.ADMIN
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            or request.method in SAFE_METHODS
        )


class ContentPermission(IsAdminOrReadOnly):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                request.user.role
                in (User.UserRole.ADMIN, User.UserRole.MODERATOR)
                or request.user.is_superuser
                or obj.author == request.user
            )
            or request.method in SAFE_METHODS
        )
