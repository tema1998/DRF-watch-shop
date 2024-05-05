from rest_framework import serializers
from .models import News, Comment


class NewsSerializer(serializers.ModelSerializer):
    """
    Serializer for News model.
    """

    likes = serializers.SerializerMethodField(method_name='get_likes')

    def get_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = News
        fields = ("id", "title", "text", "slug", "image", "created_at", "author", "likes")
        lookup_field = 'slug'
        read_only_fields = ('id', 'slug', 'created_at', 'author', 'likes')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer for list of comments.
    """

    user = serializers.SerializerMethodField(method_name='get_user')

    def get_user(self, obj):
        """
        Method for getting username of user.
        """
        return {
            "username": obj.user.username
        }

    class Meta:
        model = Comment
        fields = '__all__'


class CommentUpdateCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create and update comment model.
    """

    class Meta:
        model = Comment
        fields = [
            "id", "text", "user"
        ]
        read_only_fields = ("id", "user")

