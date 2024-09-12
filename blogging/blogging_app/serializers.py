from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [ 'title', 'author', 'content', 'published_date', 'updated_date']


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)
    class Meta:
        model = Comment
        fields = [ 'post', 'author_Comment', 'text', 'created_at']
        read_only_fields = ['created_at']
# The create method handles the creation of new Comment instances, taking care of associating the post and other validated data.
    def create(self, validated_data):
        post = validated_data.pop('post')
        comment = Comment.objects.create(post=post, **validated_data)
        return comment
