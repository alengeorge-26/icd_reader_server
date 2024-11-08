from django.urls import path
from .views import test_files,get_files, upload_file, upload_folder

urlpatterns = [
    path('test_files/', test_files,name='test_files'),
    path('get_files/', get_files,name='get_files'),
    path('upload_file/', upload_file,name='upload_file'),
    path('upload_folder/', upload_folder,name='upload_folder'),
]