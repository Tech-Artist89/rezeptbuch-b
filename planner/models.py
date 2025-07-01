from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe
from datetime import date

class MealPlan(models.Model):
    MEAL_CHOICES = [
        ('lunch', 'Mittagessen'),
        ('dinner', 'Abendessen'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='meal_plans')
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    servings = models.PositiveIntegerField(default=4, help_text="Anzahl Portionen für diese Mahlzeit")
    notes = models.TextField(blank=True, help_text="Notizen zur Mahlzeit")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'date', 'meal_type']
        ordering = ['date', 'meal_type']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.get_meal_type_display()}: {self.recipe.title}"