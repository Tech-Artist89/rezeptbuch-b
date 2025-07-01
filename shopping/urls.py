from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShoppingListViewSet, ShoppingListItemViewSet

router = DefaultRouter()
router.register(r'lists', ShoppingListViewSet, basename='shoppinglist')
router.register(r'items', ShoppingListItemViewSet, basename='shoppinglistitem')

app_name = 'shopping'
urlpatterns = [
    path('', include(router.urls)),
]