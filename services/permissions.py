from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to edit, but anyone can read.
    """

    def has_permission(self, request, view):
        # Read-only permissions for GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow editing if the user is an admin
        return request.user and request.user.is_staff
