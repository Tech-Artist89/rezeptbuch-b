from django.contrib import admin
from .models import MealPlan

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'meal_type', 'recipe', 'servings', 'created_at']
    list_filter = ['meal_type', 'date', 'user']
    search_fields = ['recipe__title', 'user__username']
    date_hierarchy = 'date'