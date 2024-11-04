from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer

@api_view(['POST'])
def login_request(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username == '' or password == '':
        return Response({'error': 'Username or password cannot be empty !!','success': False}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username !!','success': False}, status=status.HTTP_401_UNAUTHORIZED)

    if user.password == password:
        return Response({'message': 'Login successful !!','success': True}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid password !!','success': False}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_users(request):
    return Response(UserSerializer({'username': 'username', 'password': 'password'}).data)