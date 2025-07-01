from django.contrib import admin
from .models import Ingredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'calories_per_100g', 'created_at']
    search_fields = ['name']
    list_filter = ['unit']