from rest_framework.decorators import api_view, permission_classes,authentication_classes 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['POST'])
def login_request(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username == '' or password == '':
        return Response({'error': 'Username or password cannot be empty !!','success': False}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token),'refresh': str(refresh)}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid username or password !!','success': False}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def create_user(request):
    
    serializer = RegisterSerializer(data=request.data)

    if serializer.check_user_exists(request.data.get('username')):
        return Response({'error': 'Username already exists !!','success': False}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        password = request.data.get('password')
        serializer.validated_data['password'] = make_password(password)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_users(request):
    try:
        users = User.objects.all()

        data = []

        for user in users:
            data.append({
                'username': user.username,
            })

        return Response({'data': data,'success': True}, status=status.HTTP_200_OK)
    except AuthenticationFailed as e:
        return Response({'message': 'Invalid Token','success': False}, status=status.HTTP_401_UNAUTHORIZED)
