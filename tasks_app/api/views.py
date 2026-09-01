from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from board_app.models import Board
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer, CommentSerializer
from .permissions import IsBoardMember, IsTaskBoardMember, CanDeleteTask, IsCommentTaskBoardMember, IsCommentAuthor


class AssignedToMeView(GenericAPIView):
    """Return all tasks assigned to the authenticated user."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter tasks by the authenticated user as assignee."""
        return Task.objects.filter(
            assignee=self.request.user
        )

    def get(self, request):
        """Return the serialized list of assigned tasks."""
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )
        return Response(serializer.data)


class ReviewingTasksView(GenericAPIView):
    """Return all tasks reviewed by the authenticated user."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter tasks by the authenticated user as reviewer."""
        return Task.objects.filter(
            reviewer=self.request.user
        )

    def get(self, request):
        """Return the serialized list of tasks under review."""
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )
        return Response(serializer.data)


class TaskCreateView(CreateAPIView):
    """Handle the creation of tasks for a board."""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_board(self):
        """Return the board referenced in the request data."""
        board_id = self.request.data.get('board')
        return get_object_or_404(Board, pk=board_id)

    def create(self, request, *args, **kwargs):
        """Create a task and assign the authenticated user as creator."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(creator=request.user)
        output_serializer = TaskSerializer(task)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED
        )


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    """Handle retrieval, updates, and deletion of individual tasks."""

    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'task_id'

    def get_permissions(self):
        """Return permissions based on the requested task operation."""
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), CanDeleteTask()]
        return [IsAuthenticated(), IsTaskBoardMember()]

    def patch(self, request, *args, **kwargs):
        """Partially update a task and return the updated task data."""
        response = self.partial_update(request, *args, **kwargs)
        task = self.get_object()
        response.data = TaskSerializer(task).data
        return response


class CommentListCreateView(ListCreateAPIView):
    """Handle listing and creation of comments for a task."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentTaskBoardMember]

    def get_task(self):
        """Return the task referenced by the URL."""
        task_id = self.kwargs['task_id']
        return get_object_or_404(Task, pk=task_id)

    def get_queryset(self):
        """Return all comments belonging to the referenced task."""
        return self.get_task().comments.all()

    def perform_create(self, serializer):
        """Create a comment for the task with the current user as author."""
        serializer.save(
            task=self.get_task(),
            author=self.request.user
        )


class CommentDeleteView(DestroyAPIView):
    """Handle deletion of individual task comments."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        """Return comments that belong to the task referenced by the URL."""
        return Comment.objects.filter(
            task_id=self.kwargs['task_id']
        )