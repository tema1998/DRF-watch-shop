from rest_framework.permissions import BasePermission


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsStaffOrReadOnly(BasePermission):
    """
    Allows access only to admin users, or is a read-only request
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.is_staff)


class IsStaffOrOwner(BasePermission):
    """
    Allows access only to admin users, or to owner.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user and (request.user.is_staff or obj.user == request.user))
