from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile only"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to edit their own profile"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow user to update their own status only"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to update own permission"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id
