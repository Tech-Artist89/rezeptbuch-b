from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from collections import defaultdict
from .models import ShoppingList, ShoppingListItem
from .serializers import ShoppingListSerializer, ShoppingListCreateSerializer, ShoppingListItemSerializer
from planner.models import MealPlan

class ShoppingListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ShoppingListCreateSerializer
        return ShoppingListSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate_from_meal_plans(self, request, pk=None):
        """Generiert Shopping List Items basierend auf Meal Plans der Woche"""
        shopping_list = self.get_object()
        
        # Hole alle Meal Plans zwischen start_date und end_date
        meal_plans = MealPlan.objects.filter(
            user=request.user,
            date__range=[shopping_list.start_date, shopping_list.end_date]
        )
        
        if not meal_plans.exists():
            return Response(
                {'message': 'Keine Meal Plans für diesen Zeitraum gefunden'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Sammle alle Zutaten aus den Rezepten
        ingredient_totals = defaultdict(lambda: {'amount': 0, 'unit': '', 'notes': []})
        
        for meal_plan in meal_plans:
            recipe = meal_plan.recipe
            portion_factor = meal_plan.servings / recipe.servings
            
            for recipe_ingredient in recipe.recipeingredient_set.all():
                ingredient = recipe_ingredient.ingredient
                amount = recipe_ingredient.amount * portion_factor
                unit = recipe_ingredient.unit
                
                # Summiere Mengen (nur wenn gleiche Einheit)
                if (ingredient_totals[ingredient.id]['unit'] == unit or 
                    ingredient_totals[ingredient.id]['unit'] == ''):
                    ingredient_totals[ingredient.id]['amount'] += amount
                    ingredient_totals[ingredient.id]['unit'] = unit
                else:
                    # Verschiedene Einheiten - als separate Items behandeln
                    ingredient_totals[f"{ingredient.id}_{unit}"]['amount'] += amount
                    ingredient_totals[f"{ingredient.id}_{unit}"]['unit'] = unit
                    ingredient_totals[f"{ingredient.id}_{unit}"]['ingredient_id'] = ingredient.id
        
        # Erstelle Shopping List Items
        created_items = []
        for key, data in ingredient_totals.items():
            if isinstance(key, str) and '_' in key:
                ingredient_id = data['ingredient_id']
            else:
                ingredient_id = key
            
            item, created = ShoppingListItem.objects.get_or_create(
                shopping_list=shopping_list,
                ingredient_id=ingredient_id,
                defaults={
                    'amount': data['amount'],
                    'unit': data['unit'],
                    'is_purchased': False
                }
            )
            
            if not created:
                # Item existiert bereits - addiere die Menge
                item.amount += data['amount']
                item.save()
            
            created_items.append(item)
        
        return Response({
            'message': f'{len(created_items)} Items zur Einkaufsliste hinzugefügt',
            'items_count': len(created_items)
        })

class ShoppingListItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingListItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ShoppingListItem.objects.filter(
            shopping_list__user=self.request.user
        )
    
    @action(detail=True, methods=['patch'])
    def toggle_purchased(self, request, pk=None):
        """Togglet den is_purchased Status eines Items"""
        item = self.get_object()
        item.is_purchased = not item.is_purchased
        item.save()
        
        serializer = self.get_serializer(item)
        return Response(serializer.data)