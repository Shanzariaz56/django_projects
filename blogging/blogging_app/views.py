# views.py

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post, Comment
from django.contrib.auth.models import User
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt


# Example API view with JWT authentication

# Register view
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Hash the password
        )
        return Response({"message": "User registered successfully"}, status=201)
    
    # Render the register template for GET request
    return render(request, 'register.html')

# Login view
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid credentials"}, status=400)
    
    # Render the login template for GET request
    return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

# Index view
def index(request):
    return render(request, 'blogging_app/index.html')

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def showPost(request):
    posts = Post.objects.all()
    return render(request, 'blogging_app/post_list.html', {'posts': posts})

@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def addPost(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post is added successfully"}, status=201)
        else:
            return Response(serializer.errors, status=400)
    return render(request, 'blogging_app/add_post.html')

@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updatePost(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post is updated successfully"})
        return Response(serializer.errors, status=400)
    return render(request, 'blogging_app/update_post.html', {'post': post})

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def deletePost(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return Response({"message": "Post is deleted successfully"})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def write_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['post'] = post
        comment = serializer.save()
        return Response(CommentSerializer(comment).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def showComment(request):
    comments = Comment.objects.all()
    return render(request, 'blogging_app/comment_list.html', {'comments': comments})
