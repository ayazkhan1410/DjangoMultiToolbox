import os
from celery import Celery

# Set default Django settings module for the Celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediaserver.settings')

# Create Celery app with the project name
app = Celery('mediaserver')

# Configure Celery to read settings from Django's settings file, using 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in all installed Django apps
app.autodiscover_tasks()

# Example debug task to test Celery functionality
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
