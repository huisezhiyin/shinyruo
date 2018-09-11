from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shinyruo_qaq.settings')

app = Celery('shinyruo_qaq')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
