from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Allow read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_authenticated
