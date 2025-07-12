from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)


urlpatterns = router.urls

urlpatterns += [
    path('auth/token/', views.CustomAuthToken.as_view(), name='api_token_auth'),
]