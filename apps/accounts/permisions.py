from rest_framework.permissions import BasePermission

class IsOwnerAccount(BasePermission):
    """
    Allows access only to the owner of the account.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the current user is the owner of the account
        return obj.user == request.user
