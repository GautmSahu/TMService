import logging
from .constants import *

logger = logging.getLogger("django")


def send_notification(instance):
    try:
        message = f"Task '{instance.title}' assigned to {instance.assigned_to} status changed to {instance.status}."
        logger.info(message)
    except Exception as e:
        logger.error(str(e))