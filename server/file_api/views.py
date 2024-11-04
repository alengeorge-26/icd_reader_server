import os
import zipfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedFile
from .serializer import UploadedFileSerializer
import boto3
from django.conf import settings

@api_view(['GET'])
def get_files(request):
    data = {
        "message": "This is a test API in file_api",
        "success": True,
        "status": status.HTTP_200_OK
    }
    return Response(data, status=status.HTTP_200_OK)

parser_classes = (MultiPartParser, FormParser);
@api_view(['POST'])
def upload_file(request):
        file_serializer = UploadedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file = request.FILES['file']
            s3 = boto3.client('s3', 
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)
            
            bucket_name=settings.AWS_STORAGE_BUCKET_NAME
            file_key=f"uploads/{file.name}"
        
            s3.upload_fileobj(file, bucket_name, file_key,ExtraArgs={'ContentType': 'application/pdf'})

            presigned_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': file_key},
                ExpiresIn=3600 
            )

            return Response({"file_url": presigned_url}, status=201)
            
        else:
            return Response(file_serializer.errors, status=400)
        
@api_view(['POST'])
def upload_folder(request):
    pdf_url=[]

    if request.FILES.get('folder'):
        folder_zip = request.FILES['folder']
    
        s3 = boto3.client('s3', 
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME)

        bucket_name=settings.AWS_STORAGE_BUCKET_NAME

        with zipfile.ZipFile(folder_zip, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                 with zip_ref.open(file_info) as file:
                       s3_key = f"upload_folder/{file_info.filename}"
                       s3.upload_fileobj(file, bucket_name, s3_key,ExtraArgs={'ContentType': 'application/pdf'})

                       presigned_url = s3.generate_presigned_url(
                            'get_object',
                            Params={'Bucket': bucket_name, 'Key': s3_key},
                            ExpiresIn=3600 
                       )
                       pdf_url.append(presigned_url)
                      
        return Response({"message": "Folder uploaded successfully", "pdf_url": pdf_url}, status=201)
    
    else:
        return Response({"message": "No file uploaded"}, status=400)