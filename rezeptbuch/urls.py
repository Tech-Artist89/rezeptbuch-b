# rezeptbuch/urls.py - KORRIGIERTE VERSION MIT TOKEN AUTHENTICATION
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # TOKEN AUTHENTICATION ENDPOINT - DAS IST DER WICHTIGE TEIL!
    path('api/auth-token/', obtain_auth_token, name='api_token_auth'),
    
    # API URLs für die verschiedenen Apps
    path('api/users/', include('users.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/ingredients/', include('ingredients.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/planner/', include('planner.urls')),
    path('api/shopping/', include('shopping.urls')),
]