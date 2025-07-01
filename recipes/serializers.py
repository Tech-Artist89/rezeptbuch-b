from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from categories.serializers import CategorySerializer
from ingredients.serializers import IngredientSerializer

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_id', 'amount', 'unit', 'notes']

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    recipe_ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True, read_only=True
    )
    total_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions', 'prep_time', 
            'cook_time', 'total_time', 'servings', 'difficulty', 'author', 
            'categories', 'category_ids', 'recipe_ingredients', 'image', 
            'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        recipe = Recipe.objects.create(**validated_data)
        recipe.categories.set(category_ids)
        return recipe
    
    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if category_ids is not None:
            instance.categories.set(category_ids)
        
        return instance

# Einfacher Serializer für Listen-Ansichten
class RecipeListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    total_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'prep_time', 'cook_time', 
            'total_time', 'servings', 'difficulty', 'author', 
            'categories', 'image', 'is_public', 'created_at'
        ]