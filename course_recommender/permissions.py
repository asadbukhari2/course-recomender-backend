from rest_framework import permissions


class AnonPermissionOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return hasattr(user, 'student')
