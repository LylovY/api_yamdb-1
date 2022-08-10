from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешает редактировать объект только администратору
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin')
