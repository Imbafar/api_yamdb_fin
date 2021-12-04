from rest_framework import permissions


class IsUserForSelfPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff() or request.user.role == 'admin'


class IsAdminOrStaffPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.role == 'admin'


class IsAuthorOrModerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            # or request.user.is_admin
        )
