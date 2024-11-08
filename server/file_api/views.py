import zipfile
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes,authentication_classes 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializer import FileDataSerializer
from .models import FileData,Clients
from user_api.models import Users
import boto3
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_api.serializer import UserSerializer
from utils.uniqueidgen import generate_unique_id

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test_files(request):
    try:
        user_id=request.user.user_id
        user_instance = Users.objects.get(user_id=user_id)

        data = UserSerializer(user_instance).data

        data = {
            "message": "This is a test API in file_api",
            "data" : data,
            "success": True,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'message':'Test failed','success': False}, status=status.HTTP_200_OK)

parser_classes = (MultiPartParser, FormParser);
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_file(request):
    try:
        if request.FILES.get('file'):
            file = request.FILES['file']

            user_id=request.user.user_id

            user_instance = Users.objects.get(user_id=user_id)
            data = UserSerializer(user_instance).data
            client_id=data.get('client_id')

            print(client_id)

            client_instance = Clients.objects.get(client_id=client_id)

            s3 = boto3.client('s3', 
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)
            
            bucket_name=settings.AWS_STORAGE_BUCKET_NAME
            file_key=f"{client_id}/{user_id}/{file.name}"
        
            s3.upload_fileobj(file, bucket_name, file_key,ExtraArgs={'ContentType': 'application/pdf'})

            presigned_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': file_key},
                ExpiresIn=3600 
            )

            file_data = FileData.objects.create(
                file_id=f"file_{generate_unique_id()}",
                file_name=file.name,
                input_path=presigned_url,
                output_path=None,
                status=None,
                uploaded_at=datetime.now(),
                updtated_at=None,
                page_count=0,
                client_id=client_instance
            )
            return Response({'message': "File uploaded successfully","success": True,"file_url": presigned_url}, status=201)
            
        else:
            return Response({"message": "No file uploaded.Select a file","success": False}, status=400)

    except Exception as e:
        return Response({"message": "File upload failed","success": False}, status=400)
        
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_folder(request):
    try:
        pdf=[]

        user_id=request.user.user_id

        user_instance = Users.objects.get(user_id=user_id)
        data = UserSerializer(user_instance).data
        client_id=data.get('client_id')

        client_instance = Clients.objects.get(client_id=client_id)

        if request.FILES.get('folder'):
            folder_zip = request.FILES['folder']
            folder_name = folder_zip.name;

            s3 = boto3.client('s3', 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME)

            bucket_name=settings.AWS_STORAGE_BUCKET_NAME

            with zipfile.ZipFile(folder_zip, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    with zip_ref.open(file_info) as file:
                            s3_key = f"{client_id}/{user_id}/{folder_name}/{file_info.filename}"
                            
                            s3.upload_fileobj(file, bucket_name, s3_key,ExtraArgs={'ContentType': 'application/pdf'})

                            presigned_url = s3.generate_presigned_url(
                                'get_object',
                                Params={'Bucket': bucket_name, 'Key': s3_key},
                                ExpiresIn=3600 
                        )
                            
                            file_id = f"file_{generate_unique_id()}"

                            file_data = FileData.objects.create(
                                file_id=file_id,
                                file_name=file.name,
                                input_path=presigned_url,
                                output_path=None,
                                status=None,
                                uploaded_at=datetime.now(),
                                updtated_at=None,
                                page_count=0,
                                client_id=client_instance,
                            )

                            pdf.append({
                                "id": file_id,
                                "name": file_info.filename,
                                "url": presigned_url,
                                "status": "Uploaded"
                        })
                            
            return Response({"message": "Folder uploaded successfully","success": True, "pdf": pdf}, status=200)
        
        else:
            print("No folder uploaded")
            return Response({"message": "No folder uploaded","success": False}, status=400)
    
    except Exception as e:
        return Response({"message": "Folder upload failed","success": False}, status=400)
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_files(request):
    try:
        user_id=request.user.user_id

        user_instance = Users.objects.get(user_id=user_id)
        data = UserSerializer(user_instance).data

        client_id=data.get('client_id')

        file_data = FileData.objects.filter(client_id=client_id)
        file_data = FileDataSerializer(file_data, many=True).data

        data = {
            "message": "Files successfully fetched",
            "file_data" : file_data,
            "success": True,
            "status": status.HTTP_200_OK
        }
        return Response(data, status=200)
    
    except Exception as e:
        return Response({'message':'Failed to fetch files','success': False}, status=400)