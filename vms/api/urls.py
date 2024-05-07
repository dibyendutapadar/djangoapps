from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView



router = DefaultRouter()
router.register(r'vendors', VendorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

