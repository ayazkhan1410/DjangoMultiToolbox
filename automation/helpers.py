from django.apps import apps
from django.core.management.base import BaseCommand,CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
import pytz  
import os
from emails.models import Email, Sent, EmailTracking, Subscriber
import hashlib
import time
from bs4 import BeautifulSoup

def get_all_custom_models():
    default_models = ["Group", "Permission", "Session", "ContentType","LogEntry","User","Upload"]
    custom_models = []

    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if model.__name__ not in default_models:
                custom_models.append(model.__name__)
    return custom_models

def check_csv_errors(file_path,model_name):
    model = None
    
    # Search for the model across all the app
    for item in apps.get_app_configs():
        try:
            model = apps.get_model(item.label, model_name)
            break # stop searching if model found
        except LookupError:
            continue # Continue for searching app
    
    if not model:
        raise CommandError(f"Model {model_name} not Found in any app")
    
    # Compare CSV headers with model field names
    # get model fields
    model_field = [field.name for field in model._meta.fields if field.name != 'id']
    
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            
            # Compare both model fields and CSV header
            if model_field != csv_header:
                raise DataError(f"CSV File doesn't match with {model_name} table fields")
    except Exception as e:
        raise e
    
    return model

def send_email_notification(mail_subject, message, to_email, attachment=None):
    try:
        from_email = settings.EMAIL_HOST_USER
        mail = EmailMessage(mail_subject, message, from_email, to_email)
        if attachment is not None:
            mail.attach_file(attachment) # Using Build-in Function
        mail.send()
 
    except Exception as e:
        raise e

def send_email_notification_bulk(mail_subject, message, to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        for recipient_email in to_email:
            # Create EmailTracking record
            new_message = message
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)
                
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                
                email_tracking = EmailTracking.objects.create(
                    email = email,
                    subscriber = subscriber,
                    unique_id = unique_id,
                )
                
                base_url = settings.BASE_URL
                # Generate the tracking pixel url
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"

                # Search for the links in the email body
                soup = BeautifulSoup(message, 'html.parser')
                urls = [a['href'] for a in soup.find_all('a', href=True)]
                print('urls=>', urls)

                # If there are links or urls in the email body, inject our click tracking url to that original link
                if urls:
                    for url in urls:
                        # make the final tracking url
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f"{url}", f"{tracking_url}")
                else:
                    print('No URLs found in the email content')
                
                # Create the email content with tracking pixel image
                open_tracking_img = f"<img src='{open_tracking_url}' width='1' height='1'>"
                new_message += open_tracking_img

            mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email])
            
            if attachment is not None:
                mail.attach(attachment.name, attachment.read(), attachment.content_type)

            mail.content_subtype = "html"
            mail.send()
        # Store the total sent emails inside the Sent model
        if email_id:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
    except Exception as e:
        raise e

def generate_csv_filepath(model_name):
    # Get the current time in UTC and convert to 'Asia/Karachi'
    utc_now = timezone.now() 
    karachi_tz = pytz.timezone('Asia/Karachi')
    local_time = utc_now.astimezone(karachi_tz)

    # Format the local time
    formatted_time = local_time.strftime("%d-%m-%Y-%H-%M")
    
    # Folder name media/exported_data
    folder_dirs = 'exported_data'
    # Generating File Name
    file_name = f"exported_{model_name}_data_{formatted_time}.csv"
    # Generating Absolute Path
    file_path = os.path.join(settings.MEDIA_ROOT, folder_dirs, file_name)
    return file_path