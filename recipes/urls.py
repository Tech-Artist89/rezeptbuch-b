from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet

router = DefaultRouter()
router.register(r'', RecipeViewSet)

app_name = 'recipes'
urlpatterns = [
    path('', include(router.urls)),
]