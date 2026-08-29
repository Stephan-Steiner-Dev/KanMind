from django.urls import path

from .views import AssignedToMeView, ReviewingTasksView, TaskCreateView, TaskDetailView, CommentListCreateView, CommentDeleteView


urlpatterns = [
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='tasks-assigned-to-me'),
    path('tasks/reviewing/', ReviewingTasksView.as_view(), name='tasks-reviewing'),
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task-update'),
    path('tasks/<int:task_id>/comments/', CommentListCreateView.as_view(), name='task-comments'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete')
] 