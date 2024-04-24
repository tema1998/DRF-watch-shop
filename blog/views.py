from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, filters, pagination, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News, Comment
from .serializers import NewsSerializer, CommentListSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
    """
    Pagination settings for News.
    """
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class NewsViewSet(viewsets.ModelViewSet):
    """
    get:
        Returns the list of news with pagination.
    get:
        Returns the list of news with pagination.
        parameters = [slug]
    put:
        Updates an existing news. Returns updated news.
        parameters = [slug] [title, text, image]
    patch:
        Updates an existing news. Returns updated news.
        parameters = [slug] [title, text, image]
    delete:
        Delete an existing news.
        parameters = [slug]
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'text']
    filter_backends = (filters.SearchFilter,)
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    lookup_field = 'slug'
    pagination_class = PageNumberSetPagination

    def perform_create(self, serializer):
        """
        Add author to serializer
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer, *args, **kwargs):
        """
        Check: only author can edit news.
        """
        obj_author_username = News.objects.get(slug=self.kwargs['slug']).author

        if self.request.user == obj_author_username:
            serializer.save()
        else:
            raise serializers.ValidationError('Authentication error.')

    def perform_destroy(self, instance):
        """
        Check: only author can delete news.
        """
        if self.request.user == instance.author:
            instance.delete()
        else:
            raise serializers.ValidationError('Authentication error.')


class LikeNews(APIView):
    """
    post:
        Like the news.
        parameters = [slug]
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        user = request.user
        news = get_object_or_404(News, slug=slug)

        if user in news.likes.all():
            news.likes.remove(user)
        else:
            news.likes.add(user)

        return Response(
            {"ok": "Your request was successful.",
             },
            status=200,
        )


class CommentsList(APIView):
    """
    get:
        Returns the list of comments to News.
        parameters = []
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        news = get_object_or_404(News, id=id)
        query = Comment.objects.filter(news=news)
        serializer = CommentListSerializer(query, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


