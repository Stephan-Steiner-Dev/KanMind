from rest_framework import serializers

from auth_app.models import User
from board_app.models import Board
from tasks_app.models import Task


class UserSerializer(serializers.ModelSerializer):
    """Serialize basic user information."""

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'fullname'
        ]


class TaskSerializer(serializers.ModelSerializer):
    """Serialize task details including assigned users and comment count."""

    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count'
        ]

    def get_comments_count(self, obj):
        """Return the number of comments associated with the task."""
        return obj.comments.count()


class BoardSerializer(serializers.ModelSerializer):
    """Serialize board data including members and task statistics."""

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    owner_id = serializers.IntegerField(
        source='owner.id',
        read_only=True
    )

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'members',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id'
        ]

    def get_member_count(self, obj):
        """Return the number of members assigned to the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Return the total number of tasks on the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Return the number of tasks with the to-do status."""
        return obj.tasks.filter(
            status='to-do'
        ).count()

    def get_tasks_high_prio_count(self, obj):
        """Return the number of high-priority tasks on the board."""
        return obj.tasks.filter(
            priority='high'
        ).count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """Serialize detailed board data including members and tasks."""

    members = UserSerializer(
        many=True,
        read_only=True
    )

    tasks = TaskSerializer(
        many=True,
        read_only=True
    )

    owner_id = serializers.IntegerField(
        source='owner.id',
        read_only=True
    )

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'owner_id',
            'members',
            'tasks'
        ]


class BoardUpdateSerializer(serializers.ModelSerializer):
    """Serialize board updates and return detailed user information."""

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )

    owner_data = UserSerializer(
        source='owner',
        read_only=True
    )

    members_data = UserSerializer(
        source='members',
        many=True,
        read_only=True
    )

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'members',
            'owner_data',
            'members_data'
        ]