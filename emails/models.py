from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class List(models.Model):
    email_list = models.CharField(max_length=50)
    
    def __str__(self):
        return self.email_list

    def count_emails(self):
        count = Subscriber.objects.filter(email_list = self).count()
        return count
    
class Subscriber(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="subscriber_list")
    email_address = models.EmailField(max_length=40)
    
    def __str__(self):
        return self.email_address

class Email(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="list_email")
    body = models.CharField(max_length=255)
    message = RichTextUploadingField(blank=True,null=True)
    attachment = models.FileField(upload_to='email_attachments/', null=True,blank=True)
    send_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body
    
    def calculate_open_rate(self):
        total_email_sent = self.email_list.count_emails()
        opened_count = EmailTracking.objects.filter(email = self, opened_at__isnull=False).count()
        
        # Formula
        open_rate = (opened_count/total_email_sent) * 100 if total_email_sent > 0 else 0 
        return round(open_rate,2)
    
    def calculate_total_clicks(self):
        total_email_sent = self.email_list.count_emails()
        opened_click = EmailTracking.objects.filter(email = self, clicked_at__isnull=False).count()

        # Formula
        click_rate = (opened_click/total_email_sent) * 100 if total_email_sent > 0 else 0
        return round(click_rate, 2)
    
class EmailTracking(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='emaiL_tracking')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='subscriber_email_tracking')
    unique_id = models.CharField(max_length=255, unique=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.email.body
class Sent(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='sent_emails', null=True,blank=True)
    total_sent = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.email.body} - {self.total_sent} People Sent"