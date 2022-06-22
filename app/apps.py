import os

from django.apps import AppConfig as Config


class AppConfig(Config):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        from app.tasks import scheduler

        if "TIMED_TASK" in os.environ:
            scheduler.start()
