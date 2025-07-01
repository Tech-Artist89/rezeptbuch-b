from rest_framework import serializers
from .models import MealPlan
from recipes.serializers import RecipeListSerializer

class MealPlanSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    recipe = RecipeListSerializer(read_only=True)
    recipe_id = serializers.IntegerField(write_only=True)
    meal_type_display = serializers.CharField(source='get_meal_type_display', read_only=True)
    
    class Meta:
        model = MealPlan
        fields = [
            'id', 'user', 'recipe', 'recipe_id', 'date', 'meal_type', 
            'meal_type_display', 'servings', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

class MealPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = ['recipe', 'date', 'meal_type', 'servings', 'notes']