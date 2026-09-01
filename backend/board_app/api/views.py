from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsBoardMember, IsBoardOwner
from board_app.models import Board
from .serializers import (
    BoardSerializer,
    BoardDetailSerializer,
    BoardUpdateSerializer
)


class BoardViewSet(viewsets.ModelViewSet):
    """Handle CRUD operations for boards."""

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return boards owned by or assigned to the authenticated user."""
        if self.action == 'list':
            user = self.request.user
            return Board.objects.filter(
                Q(owner=user) | Q(members=user)
            ).distinct()
        return Board.objects.all()

    def get_serializer_class(self):
        """Return the appropriate serializer for the current action."""
        if self.action == 'retrieve':
            return BoardDetailSerializer
        if self.action == 'partial_update':
            return BoardUpdateSerializer
        return BoardSerializer

    def get_permissions(self):
        """Return the required permissions for the current action."""
        if self.action == 'destroy':
            return [IsAuthenticated(), IsBoardOwner()]
        if self.action in ['retrieve', 'partial_update']:
            return [IsAuthenticated(), IsBoardMember()]
        return [IsAuthenticated()]

    # def perform_create(self, serializer):
        # """Create a board and assign the authenticated user as its owner."""
        # serializer.save(owner=self.request.user)
        # board = self.get_object()

        # if board.owner != request.user:
        #     return Response(
        #         {'detail': 'Nur der Owner darf das Board löschen.'},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        # board.delete()

        # return Response(
        #     status=status.HTTP_204_NO_CONTENT
        # )


    def perform_create(self, serializer):
        """Create a board and assign the authenticated user as its owner."""
        serializer.save(owner=self.request.user)