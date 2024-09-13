from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('posts/', showPost, name='post_list'),
    path('posts/add/', addPost, name='add_post'),
    path('posts/update/<int:id>/', updatePost, name='updatePost'),
    path('posts/delete/<int:id>/', deletePost, name='deletePost'),
    path('comments/',showComment, name='showcomment'), 
    path('posts/<int:post_id>/comment/', write_comment, name='write_comment'),
     path('auth/login/', user_login, name='user_login'),
    path('auth/register/', register, name='register'),
]
