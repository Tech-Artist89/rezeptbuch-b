from django.contrib import admin
from .models import ShoppingList, ShoppingListItem

class ShoppingListItemInline(admin.TabularInline):
    model = ShoppingListItem
    extra = 1

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'start_date', 'end_date', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'start_date', 'user']
    search_fields = ['name', 'user__username']
    inlines = [ShoppingListItemInline]

@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'amount', 'unit', 'shopping_list', 'is_purchased']
    list_filter = ['is_purchased', 'shopping_list']
    search_fields = ['ingredient__name']