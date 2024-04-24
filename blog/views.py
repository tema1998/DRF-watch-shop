from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, pagination, serializers

from .models import News
from .serializers import NewsSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
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
        Check: only author can edit news..
        """
        obj_author_username = News.objects.get(slug=self.kwargs['slug']).author

        if self.request.user == obj_author_username:
            serializer.save()
        else:
            raise serializers.ValidationError('Authentication error.')
