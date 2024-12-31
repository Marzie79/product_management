from rest_framework import permissions

from authentications.models import Account


class IsOwnerOrManager(permissions.BasePermission):
    """
    Check if the user is an owner or a manager.

    Custom permission class to check if the user is an owner or a manager.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.user_type == Account.UserTypeChoices.MANAGER.value:
            return True

        return obj.owner == request.user
