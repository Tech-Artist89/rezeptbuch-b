from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'default_servings', 'created_at']
    search_fields = ['user__username', 'user__email']