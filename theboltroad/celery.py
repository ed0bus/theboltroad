import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "theboltroad.settings")

app = Celery("theboltroad")


app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "monitor-auctions-every-15-minutes": {
        "task": "monitor_auctions",
        "schedule": 900.0,
    },
}
