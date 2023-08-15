from rest_framework import permissions


class NasheedPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if user == obj.owner:
            return True

        return False
