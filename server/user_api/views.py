from rest_framework.decorators import api_view, permission_classes,authentication_classes 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer, UserCredentialsSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserCredentials,Users
from django.contrib.auth import authenticate

@api_view(['POST'])
def login_request(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username == '' or password == '':
        return Response({'error': 'Username or password cannot be empty !!','success': False}, status=status.HTTP_400_BAD_REQUEST)

    user_valid = authenticate(username=username, password=password)

    if user_valid is not None:
        user_instance = UserCredentials.objects.get(username=username)
        user_id=(UserCredentialsSerializer(user_instance).data).get('user_id')
        
        user = Users.objects.get(user_id=user_id)
        role_id=(UserSerializer(user).data).get('role_id')

        refresh = RefreshToken.for_user(user_valid) 
        refresh['user_id_id']=user_id
        refresh['role_id']=role_id
        return Response({'access': str(refresh.access_token),'refresh': str(refresh)}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid username or password !!','success': False}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def create_user(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.check_user_exists(request.data.get('username')):
        return Response({'error': 'Username already exists !!','success': False}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_users(request):
    try:
        users = UserCredentials.objects.all()
        
        data = []

        for user in users:
            data.append({
                'user_id': user.user_id,
                'username': user.username,
            })

        return Response({'data': data,'success': True}, status=status.HTTP_200_OK)
    except AuthenticationFailed as e:
        return Response({'message': 'Invalid Token','success': False}, status=status.HTTP_401_UNAUTHORIZED)