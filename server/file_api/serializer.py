from .models import UploadedFile,FileData,FileConditions
from rest_framework import serializers
class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'

class FileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileData
        fields = '__all__'

class FileConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileConditions
        fields = '__all__'