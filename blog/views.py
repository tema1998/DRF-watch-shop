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

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'text']
    filter_backends = (filters.SearchFilter,)
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    lookup_field = 'slug'
    pagination_class = PageNumberSetPagination


