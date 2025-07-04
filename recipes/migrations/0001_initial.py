# Generated by Django 5.2.3 on 2025-07-01 07:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('ingredients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('instructions', models.TextField()),
                ('prep_time', models.PositiveIntegerField(help_text='Zubereitungszeit in Minuten')),
                ('cook_time', models.PositiveIntegerField(help_text='Kochzeit in Minuten')),
                ('servings', models.PositiveIntegerField(default=4)),
                ('difficulty', models.CharField(choices=[('easy', 'Einfach'), ('medium', 'Mittel'), ('hard', 'Schwer')], default='medium', max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/')),
                ('is_public', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(related_name='recipes', to='categories.category')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('unit', models.CharField(help_text='Einheit für diese Zutat in diesem Rezept', max_length=50)),
                ('notes', models.CharField(blank=True, help_text="z.B. 'gehackt', 'in Scheiben'", max_length=200)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
            options={
                'unique_together': {('recipe', 'ingredient')},
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.RecipeIngredient', to='ingredients.ingredient'),
        ),
    ]
