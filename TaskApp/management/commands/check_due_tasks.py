import logging
from datetime import timedelta
from django.utils.timezone import now
from django.core.management.base import BaseCommand
from TaskApp.models import Task

logger = logging.getLogger("django")

class Command(BaseCommand):
    help = "Check tasks nearing their due date and log reminders."

    def handle(self, *args, **kwargs):
        try:
            """
            Finds tasks that are due in the next 24 hours and logs a reminder.
            """
            upcoming_tasks = Task.objects.select_related('assigned_to').filter(due_date__lte=now().date() + timedelta(days=1), due_date__gte=now().date())

            for task in upcoming_tasks:
                message = f"Reminder: Task '{task.title}' assigned to {task.assigned_to} is due on {task.due_date}."
                logger.info(message)
            
            self.stdout.write("Checked and logged upcoming due tasks.")
        except Exception as e:
            logger.error(str(e))