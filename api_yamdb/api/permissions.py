from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Разрешает редактировать объект только администратору или superuser
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Позволяет только авторам редактировать и удалять объект.
    Остальным просматривать.
    """

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.role == 'admin'
        )
