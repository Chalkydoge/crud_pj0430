from rest_framework import permissions
from django.contrib.auth.models import User

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.p_owner == request.user

class HasPermToWrite(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('backend.add_comment')

class HasPermToEditAndDelete(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('backend.change_comment')