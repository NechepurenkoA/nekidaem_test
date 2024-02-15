from rest_framework import permissions


class IsAuthenticatedOrAdminForUsers(permissions.IsAuthenticated):
    """Доступ к просмотру пользователей."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or obj == request.user
        )
