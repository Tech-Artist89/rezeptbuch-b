from django.db import models
from django.contrib.auth.models import User
from ingredients.models import Ingredient
from planner.models import MealPlan

class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_lists')
    name = models.CharField(max_length=200, default="Einkaufsliste")
    start_date = models.DateField(help_text="Start der Woche für die geplant wird")
    end_date = models.DateField(help_text="Ende der Woche für die geplant wird")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"


class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=50)
    is_purchased = models.BooleanField(default=False)
    notes = models.CharField(max_length=200, blank=True)
    
    # Rückverfolgung zu den Mahlzeiten, die dieses Item benötigen
    meal_plans = models.ManyToManyField(MealPlan, blank=True, related_name='shopping_items')
    
    class Meta:
        unique_together = ['shopping_list', 'ingredient']
    
    def __str__(self):
        return f"{self.amount} {self.unit} {self.ingredient.name}"