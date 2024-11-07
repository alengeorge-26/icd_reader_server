from rest_framework import serializers
from .models import UserCredentials,Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class UserCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials 
        fields = '__all__'
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials
        fields = ['user_id','username', 'password']

    def create(self, validated_data):
        user = UserCredentials.objects.create_user(
            user_id=validated_data['user_id'],
            username=validated_data['username'],    
            password=validated_data['password'],
        )
        return user
    
    def check_user_exists(self, username):
        return UserCredentials.objects.filter(username=username).exists()
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)