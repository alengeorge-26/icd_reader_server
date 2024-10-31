from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedFile
from .serializer import UploadedFileSerializer

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
            file_serializer.save()
            return Response(file_serializer.data, status=201)
        else:
            return Response(file_serializer.errors, status=400)