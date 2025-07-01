from rest_framework import serializers
from .models import ShoppingList, ShoppingListItem
from ingredients.serializers import IngredientSerializer

class ShoppingListItemSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ShoppingListItem
        fields = [
            'id', 'ingredient', 'ingredient_id', 'amount', 'unit', 
            'is_purchased', 'notes'
        ]

class ShoppingListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = ShoppingListItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    purchased_items = serializers.SerializerMethodField()
    
    class Meta:
        model = ShoppingList
        fields = [
            'id', 'user', 'name', 'start_date', 'end_date', 'is_completed',
            'items', 'total_items', 'purchased_items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_total_items(self, obj):
        return obj.items.count()
    
    def get_purchased_items(self, obj):
        return obj.items.filter(is_purchased=True).count()

class ShoppingListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ['name', 'start_date', 'end_date']