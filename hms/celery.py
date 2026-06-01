import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')

try:
    from celery import Celery
    app = Celery('hms')
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()
except ImportError:
    app = None