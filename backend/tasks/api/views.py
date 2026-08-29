from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from board.models import Board
from tasks.models import Task, Comment
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer, CommentSerializer
from .permissions import IsBoardMember, IsTaskBoardMember, CanDeleteTask, IsCommentTaskBoardMember, IsCommentAuthor


class AssignedToMeView(GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            assignee=self.request.user
        )

    def get(self, request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )
        return Response(serializer.data)


class ReviewingTasksView(GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            reviewer=self.request.user
        )

    def get(self, request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )
        return Response(serializer.data)


class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_board(self):
        board_id = self.request.data.get('board')
        return get_object_or_404(Board, pk=board_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(creator=request.user)
        output_serializer = TaskSerializer(task)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED
        )


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'task_id'

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), CanDeleteTask()]
        return [IsAuthenticated(), IsTaskBoardMember()]

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        task = self.get_object()
        response.data = TaskSerializer(task).data
        return response


class CommentListCreateView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentTaskBoardMember]

    def get_task(self):
        task_id = self.kwargs['task_id']
        return get_object_or_404(Task, pk=task_id)

    def get_queryset(self):
        return self.get_task().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            task=self.get_task(),
            author=self.request.user
        )


class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        return Comment.objects.filter(
            task_id=self.kwargs['task_id']
        )