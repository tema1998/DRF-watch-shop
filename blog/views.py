from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, filters, pagination, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News, Comment
from .permissions import IsStaffOrReadOnly, IsStaffOrOwner
from .serializers import NewsSerializer, CommentListSerializer, CommentUpdateCreateSerializer


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
        Returns the news by slug.
        parameters = [slug]
    post:
        Create the news. Returns created news.
        parameters = [slug] [title, text, image]
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
    permission_classes = [IsStaffOrReadOnly]
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


class LikeNews(APIView):
    """
    post:
        Like the news.
        parameters = [slug]
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        news = get_object_or_404(News, pk=pk)

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
        parameters = [news_id]
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        query = Comment.objects.filter(news=news)
        serializer = CommentListSerializer(query, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CommentCreate(APIView):
    """
    post:
        Create a comment instance to News. Returns created comment data.
        parameters: [news_id, text]
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CommentUpdateCreateSerializer(data=request.data)

        if serializer.is_valid():
            news = get_object_or_404(News, pk=serializer.data.get('news_id'))
            comment = Comment.objects.create(
                text=serializer.data.get('text'),
                news=news,
                user=request.user,
            )
            return Response(
                CommentUpdateCreateSerializer(comment).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CommentUpdateDelete(APIView):
    """
    put:
        Update an existing comment. Returns updated comment data.

        parameters: [pk, text]

    delete:
        Delete an existing comment.

        parameters: [pk]
    """

    permission_classes = [IsStaffOrOwner]

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentUpdateCreateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)