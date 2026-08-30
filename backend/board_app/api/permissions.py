from rest_framework.permissions import BasePermission


class IsBoardMember(BasePermission):
    """Allow access only to users who own or are members of the board."""

    message = 'You must be a member of this board.'

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user belongs to the board."""
        return (
            obj.owner_id == request.user.id
            or obj.members.filter(id=request.user.id).exists()
        )


class IsBoardOwner(BasePermission):
    """Allow access only to the owner of the board."""

    message = 'Only the board owner can perform this action.'

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user is the board owner."""
        return obj.owner_id == request.user.id