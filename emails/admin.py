from django.contrib import admin
from emails.models import *

@admin.register(List)
class AdminList(admin.ModelAdmin):
    list_display = ['email_list']
    list_per_page = 30
    search_fields = ['email_list']

@admin.register(Subscriber)
class AdminSubscriber(admin.ModelAdmin):
    list_display = ['email_list', 'email_address']
    list_per_page = 30
    search_fields = ['email_address']
    
@admin.register(Email)
class AdminEmail(admin.ModelAdmin):
    list_display = ['email_list', 'body', 'message', 'attachment', 'send_at', ]
    list_per_page = 30
    search_fields = ['body', 'message']

@admin.register(EmailTracking)
class AdminEmailTracking(admin.ModelAdmin):
    list_display = ['email', 'subscriber', 'unique_id', 'opened_at', 'clicked_at' ]
    search_fields = ['unique_id']
    list_per_page = 50

@admin.register(Sent)
class AdminSent(admin.ModelAdmin):
    list_display = ['email','total_sent']
    search_fields = ['email']
    list_per_page = 50