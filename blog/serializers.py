from rest_framework import serializers
from .models import News, Comment
from django.contrib.auth.models import User


class NewsSerializer(serializers.ModelSerializer):
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
    user = serializers.SerializerMethodField(method_name='get_user')

    def get_user(self, obj):
        return {
            "username": obj.user.username
        }

    class Meta:
        model = Comment
        fields = '__all__'


class CommentUpdateCreateSerializer(serializers.ModelSerializer):
    news_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = [
            "id", "news_id", "text", "user"
        ]
        read_only_fields = ("id", "user",)

