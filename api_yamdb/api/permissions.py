from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешает редактировать объект только администратору
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin')


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Позволяет только авторам редактировать и удалять объект.
    Остальным просматривать.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
