from django.apps import AppConfig


class TaskappConfig(AppConfig):
    name = 'TaskApp'

    def ready(self):
        import TaskApp.signals