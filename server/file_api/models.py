from django.db import models
from user_api.models import Clients,Projects

class FileData(models.Model):
    file_id = models.CharField(primary_key=True,max_length=50)
    file_name = models.CharField(max_length=200,default=None,blank=False,null=False)
    input_path = models.CharField(max_length=500,default=None)
    output_path = models.CharField(max_length=500,default=None,null=True)
    status = models.CharField(max_length=100,default=None,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True)
    updtated_at = models.DateTimeField(auto_now=True)
    page_count = models.IntegerField(default=0)

    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)

    class Meta:
        db_table = 'file_data'

    def __str__(self):
        return self.file_name

class FileConditions(models.Model):
    file_id = models.ForeignKey(FileData, on_delete=models.CASCADE,max_length=50)
    condition = models.CharField(max_length=1000,null=True)

    class Meta:
        db_table = 'conditions'

    def __str__(self):
        return self.condition  
    
class UploadedFile(models.Model):
    user_id = models.CharField(max_length=100,default=None)
    input_path = models.CharField(max_length=200,default=None)
    output_path = models.CharField(max_length=200,default=None,null=True)
    status = models.CharField(max_length=100,default=None,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)