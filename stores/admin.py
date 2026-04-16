"""
Store admin configuration
"""
from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'status', 'products_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description', 'owner__username']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
