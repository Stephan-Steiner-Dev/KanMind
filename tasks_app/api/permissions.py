from rest_framework.permissions import BasePermission


class IsBoardMember(BasePermission):
    """Allow access only to users who own or are members of the board."""

    message = 'You must be a member of this board.'

    def has_permission(self, request, view):
        """Check whether the requesting user belongs to the board."""
        board = view.get_board()
        return (
            board.owner_id == request.user.id
            or board.members.filter(id=request.user.id).exists()
        )


class IsTaskBoardMember(BasePermission):
    """Allow access only to users who belong to the task's board."""

    message = 'You must be a member of this board.'

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user belongs to the task's board."""
        board = obj.board
        return (
            
            board.owner_id == request.user.id
            or board.members.filter(id=request.user.id).exists()
        )


class CanDeleteTask(BasePermission):
    """Allow task deletion only by the task creator or board owner."""

    message = 'Only the task creator or board owner can delete this task.'

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user is allowed to delete the task."""
        return (
            obj.creator_id == request.user.id
            or obj.board.owner_id == request.user.id
        )


class IsCommentTaskBoardMember(BasePermission):
    """Allow comment access only to users who belong to the task's board."""

    message = 'You must be a member of this board.'

    def has_permission(self, request, view):
        """Check whether the requesting user belongs to the task's board."""
        task = view.get_task()
        board = task.board
        return (
            board.owner_id == request.user.id
            or board.members.filter(id=request.user.id).exists()
        )


class IsCommentAuthor(BasePermission):
    """Allow comment deletion only by the comment author."""

    message = 'Only the comment author can delete this comment.'

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user is the comment author."""
        return obj.author_id == request.user.id