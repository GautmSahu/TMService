from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from NotificationApp.utils import send_notification
import logging

logger = logging.getLogger("django")

@receiver(post_save, sender=Task)
def task_updated(sender, instance, created, **kwargs):
    try:
        if not created:
            send_notification(instance)
    except Exception as e:
        logger.error(str(e))