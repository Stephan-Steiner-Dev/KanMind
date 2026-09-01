from django.conf import settings
from django.db import models

from board_app.models import Board


class Task(models.Model):
    """Represent a task assigned to a board."""

    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='review_tasks'
    )

    due_date = models.DateField()

    def __str__(self):
        """Return the task title as its string representation."""
        return self.title


class Comment(models.Model):
    """Represent a comment associated with a task."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        """Return the comment ID as its string representation."""
        return f'Comment {self.id}'