from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RegisterView, ProfileView, FeedbackView, ReviewsView, Cart, AddProductToCart, \
    RemoveProductFromCart, CreatePaymentView

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path("", include(router.urls)),
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('feedback/', FeedbackView.as_view(), name="feedback"),
    path("reviews/", ReviewsView.as_view(), name="reviews"),
    path("reviews/<slug:product_slug>/", ReviewsView.as_view(), name="reviews_for_product"),
    path("cart/", Cart.as_view(), name="cart"),
    path("cart/add/", AddProductToCart.as_view(), name="cart_add"),
    path("cart/remove/", RemoveProductFromCart.as_view(), name="cart_remove"),
    path("cart/payment/create/", CreatePaymentView.as_view(), name="create_payment"),
]