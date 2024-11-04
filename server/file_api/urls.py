from django.urls import path
from .views import get_files, upload_file, upload_folder

urlpatterns = [
    path('file_test/', get_files,name='get_files'),
    path('upload_file/', upload_file,name='upload_file'),
    path('upload_folder/', upload_folder,name='upload_folder'),
]