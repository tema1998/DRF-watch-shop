from django.shortcuts import render
from rest_framework import viewsets, permissions, pagination, filters, generics, mixins
from .serializers import ProductSerializer, RegisterSerializer, UserSerializer, FeedbackSerializer, ReviewsSerializer
from .models import Product, Feedback, Reviews
from rest_framework.response import Response


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['model', 'brand']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
    pagination_class = PageNumberSetPagination


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Success",
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(request.user,
                                   context=self.get_serializer_context()).data,
        })


class FeedbackView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class ReviewsView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        product_slug = self.kwargs['product_slug'].lower()
        product = Product.objects.get(slug=product_slug)
        return Reviews.objects.filter(product=product)
