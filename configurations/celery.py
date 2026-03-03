import os
from datetime import timedelta

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings.local")
app = Celery("configurations", broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"))
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     "fetch-currency-stats-every-minute": {
#         "task": "app.tasks.fetch_stats_task",
#         "schedule": timedelta(seconds=30),
#     },
#     "fetch-blocks-every-min": {
#         "task": "app.tasks.fetch_blocks_task",
#         "schedule": timedelta(seconds=30),
#     },
# }
