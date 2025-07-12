from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView 
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)


urlpatterns = router.urls

urlpatterns += [
    path('auth/token/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('schema/', SpectacularAPIView.as_view(), name='api_schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='api_schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='api_schema'), name='redoc'),
]