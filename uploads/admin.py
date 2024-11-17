from django.contrib import admin
from .models import Upload

@admin.register(Upload)
class AdminUpload(admin.ModelAdmin):
    list_display = ['file', 'model_name', 'uploaded_at']
    list_per_page = 30
    
    