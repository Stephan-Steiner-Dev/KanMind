from rest_framework import serializers

from auth_app.models import User
from tasks.models import Task, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'fullname',
        ]


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count',
        ]

    def get_comments_count(self, obj):
        return 0


class TaskCreateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        required=False,
        allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'due_date',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        board = attrs['board']
        self._validate_user(attrs.get('assignee'), board, 'assignee')
        self._validate_user(attrs.get('reviewer'), board, 'reviewer')
        return attrs

    def _validate_user(self, user, board, field):
        if user and not self._belongs_to_board(user, board):
            raise serializers.ValidationError(
                {field: 'User is not a member of this board.'}
            )

    def _belongs_to_board(self, user, board):
        return (
            board.owner_id == user.id
            or board.members.filter(id=user.id).exists()
        )


class TaskUpdateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        required=False,
        allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'due_date',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        board = self.instance.board
        self._validate_user(attrs.get('assignee'), board, 'assignee_id')
        self._validate_user(attrs.get('reviewer'), board, 'reviewer_id')
        return attrs

    def _validate_user(self, user, board, field):
        if user and not self._belongs_to_board(user, board):
            raise serializers.ValidationError(
                {field: 'User is not a member of this board.'}
            )

    def _belongs_to_board(self, user, board):
        return (
            board.owner_id == user.id
            or board.members.filter(id=user.id).exists()
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.fullname',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'created_at',
            'author',
            'content',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'author',
        ]