from mediaserver.celery import app
import time
from django.core.management import call_command, CommandError
from django.core.mail import EmailMessage
from django.conf import settings
from automation.helpers import send_email_notification_bulk
from .models import *

@app.task
def celery_bulk_email_send(body, message, to_email, attachment,email_id):
    try:
        send_email_notification_bulk(body, message, to_email, attachment,email_id)
    except Exception as e:
        raise e
    
    return 'Task done and email sent successfully'
