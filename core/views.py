from django.shortcuts import render
from django.views.generic.base import ContextMixin
from rest_framework import viewsets, permissions, pagination, filters, generics, mixins, serializers, status
from rest_framework.views import APIView

from .permissions import IsStaffOrReadOnly
from .serializers import ProductSerializer, RegisterSerializer, UserSerializer, FeedbackSerializer, ReviewsSerializer, \
    CartSerializer, AddProductToCartSerializer, RemoveProductFromCartSerializer
from .models import Product, Feedback, Reviews, Order
from rest_framework.response import Response


class PageNumberSetPagination(pagination.PageNumberPagination):
    """
    Pagination settings for Products.
    """
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class ProductViewSet(viewsets.ModelViewSet):
    """
    get:
        Returns the list of products with pagination.
    get:
        Returns the product by slug.
        parameters = [slug]
    post:
        Create a product. Returns created product.
        parameters = [slug] [brand, model, description, image, price, discount]
    put:
        Updates an existing product. Returns updated product.
        parameters = [slug] [brand, model, description, image, price, discount]
    patch:
        Updates an existing product. Returns updated product.
        parameters = [slug] [brand, model, description, image, price, discount]
    delete:
        Delete an existing product.
        parameters = [slug]
    """

    permission_classes = [IsStaffOrReadOnly]
    search_fields = ['model', 'brand']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-created_at')
    lookup_field = 'slug'
    pagination_class = PageNumberSetPagination


class RegisterView(generics.GenericAPIView):
    """
    post:
        Create user account. Returns created account.
        parameters = [username, password, password2]
    """

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
    """
    get:
        Returns profile data of current user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(request.user,
                                   context=self.get_serializer_context()).data,
        })


class FeedbackView(generics.ListCreateAPIView):
    """
    get:
        Returns the list of feedbacks.
    post:
        Create feedback. Returns created feedback.
        parameters = [review, image]
    """

    permission_classes = [permissions.AllowAny]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        """
        Add author to serializer
        """
        serializer.save(user=self.request.user)


class ReviewsView(generics.ListCreateAPIView):
    """
    get:
        Returns the list of reviews to product by slug.
        parameters = [product_slug]
    post:
        Create review. Returns created review.
        parameters = [product_id, text]
    """
    permission_classes = [permissions.AllowAny]
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        product_slug = self.kwargs['product_slug'].lower()
        product = Product.objects.get(slug=product_slug)
        return Reviews.objects.filter(product=product)

    def perform_create(self, serializer):
        """
        Add author to serializer
        """
        serializer.save(user=self.request.user)


class Cart(APIView):
    """
    get:
    Get product from the cart of current user.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Order.objects.filter(user=request.user, is_ordered=False)
        if queryset:
            serializer = CartSerializer(queryset[0])
            return Response(serializer.data)
        return Response("your cart is empty", status=status.HTTP_403_FORBIDDEN)


class AddProductToCart(generics.CreateAPIView):
    """
    post:
    Add product to cart of current user.
    parameters = [product_id]
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddProductToCartSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response("The product was successfully added to cart.", status=status.HTTP_201_CREATED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        return context


class RemoveProductFromCart(APIView):
    """
    post:
    Remove product from cart of current user.
    parameters = [product_id]
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RemoveProductFromCartSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        response_message = serializer.save()
        return Response(response_message)


