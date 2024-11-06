from django.db import models

class UploadedFile(models.Model):
    user_id = models.CharField(max_length=100,default=None)
    input_path = models.CharField(max_length=200,default=None)
    output_path = models.CharField(max_length=200,default=None,null=True)
    status = models.CharField(max_length=100,default=None)
    uploaded_at = models.DateTimeField(auto_now_add=True)