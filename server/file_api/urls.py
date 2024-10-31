from django.urls import path
from .views import get_files, upload_file

urlpatterns = [
    path('file_test/', get_files,name='get_files'),
    path('upload_file/', upload_file,name='upload_file'),
]