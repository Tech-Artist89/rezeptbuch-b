# users/urls.py (aktualisiert)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

app_name = 'users'
urlpatterns = [
    # Standard ViewSet URLs
    path('', include(router.urls)),
    
    # Auth URLs
    path('auth/', include('users.auth_urls')),
]