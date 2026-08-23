from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from board.models import Board
from .serializers import (
    BoardSerializer,
    BoardDetailSerializer,
    BoardUpdateSerializer
)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Board.objects.filter(
            Q(owner=user) |
            Q(members=user)
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardDetailSerializer

        if self.action == 'partial_update':
            return BoardUpdateSerializer

        return BoardSerializer

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
        board = self.get_object()

        if board.owner != request.user:
            return Response(
                {'detail': 'Nur der Owner darf das Board löschen.'},
                status=status.HTTP_403_FORBIDDEN
            )

        board.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )