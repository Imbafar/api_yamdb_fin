from rest_framework import permissions

from reviews.models import CustomUser


class IsUserForSelfPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminOrStaffPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or (
                request.user.is_authenticated
                and request.user.role == CustomUser.USER_ROLE_ADMIN)
        )


class IsAuthorOrModerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_authenticated and (
                request.user.role == CustomUser.USER_ROLE_ADMIN
                or request.user.role == CustomUser.USER_ROLE_MODERATOR)
                )
        )


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.role == CustomUser.USER_ROLE_ADMIN)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.role == CustomUser.USER_ROLE_ADMIN)
        )
