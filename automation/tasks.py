from mediaserver.celery import app
import time
from django.core.management import call_command, CommandError
from django.core.mail import EmailMessage
from django.conf import settings
from .helpers import send_email_notification, generate_csv_filepath

@app.task
def celery_email_send():
    time.sleep(5)
    mail_subject = "Test Email"
    message =  "Testing purposes"
    to_email = ['ayazbadsha786@gmail.com']
    send_email_notification(mail_subject, message,to_email)
    return 'Email sent Successfully'
    
@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except CommandError as ce:
        raise ce  
    except Exception as e:  
        raise e
    
    # Once importdata has been completed then we sent the email
    mail_subject = "Import Successful"
    message =  "Your Data has been imported Successfully ..."
    to_email = ['ayazbadsha786@gmail.com']
    send_email_notification(mail_subject, message, to_email)
    
    return 'Data imported Successfully'

@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e
    
    # Once ExportData has been completed then we sent the email
    file_path = generate_csv_filepath(model_name)
    mail_subject = "Data Exported Successful"
    message =  "Your Data has been Exported Successfully. Please find attachment"
    to_email = ['ayazbadsha786@gmail.com']
    send_email_notification(mail_subject, message, to_email, attachment=file_path)
    
    return 'Data Exported Successful'