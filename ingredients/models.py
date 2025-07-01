from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    unit = models.CharField(max_length=50, help_text="Standard-Einheit (g, ml, Stück, etc.)")
    calories_per_100g = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.unit})"