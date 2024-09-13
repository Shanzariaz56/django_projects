# views.py
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404, render
from .authentication import authenticate_user, jwt_required
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Register View
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
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

# Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    token = authenticate_user(username, password)
    if token:
        return Response({'token': token}, status=200)
    else:
        return Response({"error": "Invalid credentials"}, status=400)

# Index View
def index(request):
    return render(request, 'blogging_app/index.html')

# Show All Posts (JWT Protected)
@api_view(['GET'])
@jwt_required
def showPost(request):
    print("poiuioiuio")
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# Add Post (JWT Protected)
@api_view(['POST'])
@jwt_required
def addPost(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Post is added successfully"}, status=201)
    return Response(serializer.errors, status=400)

# Update Post (JWT Protected)
@api_view(['POST', 'GET'])
@jwt_required
def updatePost(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post is updated successfully"})
        return Response(serializer.errors, status=400)

# Delete Post (JWT Protected)
@api_view(['DELETE'])
@jwt_required
def deletePost(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return Response({"message": "Post is deleted successfully"})

# Write Comment on a Post (JWT Protected)
@api_view(['POST'])
@jwt_required
def write_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['post'] = post
        comment = serializer.save()
        return Response(CommentSerializer(comment).data, status=201)
    return Response(serializer.errors, status=400)

# Show All Comments (JWT Protected)
@api_view(['GET'])
@jwt_required
def showComment(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
