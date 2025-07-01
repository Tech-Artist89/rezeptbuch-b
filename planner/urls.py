from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealPlanViewSet

router = DefaultRouter()
router.register(r'', MealPlanViewSet, basename='mealplan')

app_name = 'planner'
urlpatterns = [
    path('', include(router.urls)),
]