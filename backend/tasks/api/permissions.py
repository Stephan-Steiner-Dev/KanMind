from rest_framework.permissions import BasePermission


class IsBoardMember(BasePermission):
    message = 'You must be a member of this board.'

    def has_permission(self, request, view):
        board = view.get_board()
        return (
            board.owner_id == request.user.id
            or board.members.filter(id=request.user.id).exists()
        )


class IsTaskBoardMember(BasePermission):
    message = 'You must be a member of this board.'

    def has_object_permission(self, request, view, obj):
        board = obj.board
        return (
            board.owner_id == request.user.id
            or board.members.filter(id=request.user.id).exists()
        )


class CanDeleteTask(BasePermission):
    message = 'Only the task creator or board owner can delete this task.'

    def has_object_permission(self, request, view, obj):
        return (
            obj.creator_id == request.user.id
            or obj.board.owner_id == request.user.id
        )


class IsCommentTaskBoardMember(BasePermission):
    message = 'You must be a member of this board.'

    def has_permission(self, request, view):
        task = view.get_task()
        board = task.board
        return (
            board.owner_id == request.user.id
            or board.members.filter(id=request.user.id).exists()
        )


class IsCommentAuthor(BasePermission):
    message = 'Only the comment author can delete this comment.'

    def has_object_permission(self, request, view, obj):
        return obj.author_id == request.user.id