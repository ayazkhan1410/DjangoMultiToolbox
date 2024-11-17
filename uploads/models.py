from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Upload(models.Model):
    file = models.FileField(upload_to='uploads/files/')
    model_name = models.CharField(max_length=50, null=True,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.file.size > 10 * 1024 * 1024: 
            raise ValidationError(_('File size must be under 2 MB.'))

    def __str__(self):
        return f'{self.file} - {self.model_name}'
    