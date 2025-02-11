from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import NewsViewSet, LikeNews, CommentsList, CommentCreate, CommentUpdateDelete

app_name = 'blog'
router = DefaultRouter()
router.register('news', NewsViewSet, basename='news')

urlpatterns = [
    path("", include(router.urls)),
    path("like/<int:pk>/", LikeNews.as_view(), name="like"),
    path("comments/<int:pk>/", CommentsList.as_view(), name="comments"),
    path("comments/create/", CommentCreate.as_view(), name="comments-create"),
    path("comments/update-delete/<int:pk>/", CommentUpdateDelete.as_view(), name="comments-update-delete"),
]