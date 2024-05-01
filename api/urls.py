from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="Watch-shop API",
      default_version='v1',
      description="Watch-shop",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="artemvol1998@gmail.com"),
      license=openapi.License(name="tema1998"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("ckeditor/", include('ckeditor_uploader.urls')),
    path('api/core/', include('core.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/payment/', include('payment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

