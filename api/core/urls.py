from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RegisterView, ProfileView, FeedbackView, ReviewsView

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path("", include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('feedback/', FeedbackView.as_view()),
    path("reviews/", ReviewsView.as_view()),
    path("reviews/<slug:product_slug>/", ReviewsView.as_view()),
]