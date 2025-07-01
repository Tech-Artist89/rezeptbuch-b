from django.contrib import admin
from .models import Recipe, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'difficulty', 'prep_time', 'cook_time', 'servings', 'is_public', 'created_at']
    list_filter = ['difficulty', 'is_public', 'categories', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['categories']
    inlines = [RecipeIngredientInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # Nur bei neuen Objekten
            obj.author = request.user
        super().save_model(request, obj, form, change)
