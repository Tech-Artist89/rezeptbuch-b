# users/auth_views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .serializers import UserSerializer
from .models import UserProfile

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login View - Entspricht dem Frontend AuthService.login()
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # User authentifizieren
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
        return Response({
            'error': 'Account is disabled'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Token erstellen oder abrufen
    token, created = Token.objects.get_or_create(user=user)
    
    # User Serializer
    user_serializer = UserSerializer(user)
    
    return Response({
        'token': token.key,
        'user': user_serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register View - Für User-Registrierung
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    
    # Validation
    if not username or not email or not password:
        return Response({
            'error': 'Username, email and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(password) < 6:
        return Response({
            'error': 'Password must be at least 6 characters long'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return Response({
            'error': 'Username already exists'
        }, status=status.HTTP_409_CONFLICT)
    
    if User.objects.filter(email=email).exists():
        return Response({
            'error': 'Email already exists'
        }, status=status.HTTP_409_CONFLICT)
    
    try:
        # User erstellen
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # UserProfile automatisch erstellen
        UserProfile.objects.create(user=user)
        
        # Token erstellen
        token = Token.objects.create(user=user)
        
        # User Serializer
        user_serializer = UserSerializer(user)
        
        return Response({
            'token': token.key,
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except IntegrityError:
        return Response({
            'error': 'User creation failed'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])  # oder IsAuthenticated falls nur eingeloggte User sich ausloggen können
def logout_view(request):
    """
    Logout View - Token löschen
    """
    try:
        # Token aus Request holen
        token_key = request.auth
        if token_key:
            token = Token.objects.get(key=token_key)
            token.delete()
        
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
        
    except Token.DoesNotExist:
        return Response({
            'message': 'Already logged out'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_username(request):
    """
    Username Verfügbarkeit prüfen (für Register-Form)
    """
    username = request.data.get('username')
    
    if not username:
        return Response({
            'error': 'Username is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exists = User.objects.filter(username=username).exists()
    
    return Response({
        'available': not exists,
        'username': username
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_email(request):
    """
    Email Verfügbarkeit prüfen (für Register-Form)
    """
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exists = User.objects.filter(email=email).exists()
    
    return Response({
        'available': not exists,
        'email': email
    }, status=status.HTTP_200_OK)