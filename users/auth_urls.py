# users/auth_urls.py (neue Datei erstellen)
from django.urls import path
from .auth_views import login_view, register_view, logout_view, check_username, check_email

urlpatterns = [
    path('login/', login_view, name='auth-login'),
    path('register/', register_view, name='auth-register'),
    path('logout/', logout_view, name='auth-logout'),
    path('check-username/', check_username, name='check-username'),
    path('check-email/', check_email, name='check-email'),
]