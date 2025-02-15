from django.db import models
from UserApp.models import CustomUser

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField()
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['id', 'status', 'due_date', 'assigned_to']),
        ]