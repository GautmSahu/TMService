from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import *
from django_filters.rest_framework import DjangoFilterBackend

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrAssignedUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'due_date']

    def get_queryset(self):
        """Admins see all tasks, regular users see only their assigned tasks."""
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.all()
        return Task.objects.select_related('assigned_to').filter(assigned_to=user)