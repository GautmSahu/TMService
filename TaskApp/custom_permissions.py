from rest_framework import permissions

class IsAdminOrAssignedUser(permissions.BasePermission):
    """
    Custom permission:
    - Admins can create, update, delete, and view all tasks.
    - Regular users can only view tasks assigned to them.
    """

    def has_permission(self, request, view):
        # Allow all authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins can access everything
        if request.user.role == 'admin':
            return True
        # Regular users can only view their assigned tasks
        return obj.assigned_to == request.user