from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet

router = DefaultRouter()
router.register(r'', IngredientViewSet)

app_name = 'ingredients'
urlpatterns = [
    path('', include(router.urls)),
]