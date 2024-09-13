import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed

def generate_jwt_token(user):
    """
    Generates a JWT token.
    """
    payload = {
        'id': user.pk,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=360),  # Token expiration time
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm=settings.SIMPLE_JWT['ALGORITHM'])
    return token

def authenticate_user(username, password):
    """
    Authenticates the user and returns a JWT token if successful.
    """
    user = authenticate(username=username, password=password)
    if user is not None:
        token = generate_jwt_token(user)
        return token
    return None

def decode_jwt_token(token):
    """
    Decodes the JWT token and returns the user if the token is valid.
    """
    try:
        payload = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        user = User.objects.get(id=payload['id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        raise AuthenticationFailed('Invalid or expired token')

def jwt_required(view_func):
    """
    Decorator that ensures JWT token is valid and attaches the user to the request.
    """
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        
        if not auth_header:
            raise AuthenticationFailed('Token is missing')
        try:
            token = auth_header.split(' ')[1]  # Expecting token in 'Bearer <token>' format
            user = decode_jwt_token(token)
            request.user = user
        except IndexError:
            raise AuthenticationFailed('Token is malformed')
        except AuthenticationFailed:
            raise AuthenticationFailed('Invalid or expired token')
        return view_func(request, *args, **kwargs)
    
    return wrapper
