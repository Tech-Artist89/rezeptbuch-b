from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from ingredients.models import Ingredient

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Einfach'),
        ('medium', 'Mittel'),
        ('hard', 'Schwer'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    prep_time = models.PositiveIntegerField(help_text="Zubereitungszeit in Minuten")
    cook_time = models.PositiveIntegerField(help_text="Kochzeit in Minuten")
    servings = models.PositiveIntegerField(default=4)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    
    # Beziehungen
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    categories = models.ManyToManyField(Category, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')
    
    # Zusätzliche Felder
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def total_time(self):
        return self.prep_time + self.cook_time


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=50, help_text="Einheit für diese Zutat in diesem Rezept")
    notes = models.CharField(max_length=200, blank=True, help_text="z.B. 'gehackt', 'in Scheiben'")
    
    class Meta:
        unique_together = ['recipe', 'ingredient']
    
    def __str__(self):
        return f"{self.amount} {self.unit} {self.ingredient.name}"