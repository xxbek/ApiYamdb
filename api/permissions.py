from rest_framework import permissions


class ReadAnyChangeAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser():
            return True


class ReadOnlyOrAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user or request.user.is_superuser():
            return True

        return False
