"""
AI Assistant admin configuration
"""
from django.contrib import admin
from .models import AIRequest


@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'request_type', 'tokens_used', 'processing_time', 'created_at']
    list_filter = ['request_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
