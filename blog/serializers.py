from rest_framework import serializers
from .models import News
from django.contrib.auth.models import User


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ("id", "title", "text", "slug", "image", "created_at", "author")
        lookup_field = 'slug'
        read_only_fields = ('id', 'slug', 'created_at', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }