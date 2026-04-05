from rest_framework.permissions import BasePermission
from .models import Role


class IsAdmin(BasePermission):
    """Only admin role users can pass."""
    message = 'You do not have permission. Admin role required.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == Role.ADMIN
        )


class IsAnalystOrAdmin(BasePermission):
    """Analyst and admin roles can pass."""
    message = 'You do not have permission. Analyst or Admin role required.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in (Role.ANALYST, Role.ADMIN)
        )


class IsViewer(BasePermission):
    """Any authenticated user can pass (viewer is the minimum role)."""
    message = 'Authentication required.'

    def has_permission(self, request, view):
        return request.user.is_authenticated