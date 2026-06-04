"""
Enhanced AI Assistant admin configuration
"""
from django.contrib import admin
from .models import (
    AIRequest, ConversationSession, ConversationMessage,
    AIRecommendation, WebSearchCache
)


@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'request_type', 'tokens_used', 'processing_time', 'created_at']
    list_filter = ['request_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']


@admin.register(ConversationSession)
class ConversationSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'language', 'message_count', 'tokens_used', 'is_active', 'updated_at']
    list_filter = ['language', 'is_active', 'created_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'language', 'is_active')
        }),
        ('Statistics', {
            'fields': ('message_count', 'tokens_used')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Context', {
            'fields': ('context',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ['get_session_title', 'role', 'created_at']
    list_filter = ['role', 'created_at', 'session__language']
    search_fields = ['session__title', 'content']
    readonly_fields = ['created_at']
    
    def get_session_title(self, obj):
        return obj.session.title or f'Session {obj.session.id}'
    get_session_title.short_description = 'Session'


@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'recommendation_type', 'language', 'confidence_score', 'clicked', 'created_at']
    list_filter = ['recommendation_type', 'language', 'clicked', 'created_at']
    search_fields = ['user__username', 'title', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'description', 'recommendation_type', 'language')
        }),
        ('Details', {
            'fields': ('reason', 'confidence_score', 'data')
        }),
        ('Tracking', {
            'fields': ('clicked', 'created_at')
        }),
    )


@admin.register(WebSearchCache)
class WebSearchCacheAdmin(admin.ModelAdmin):
    list_display = ['query', 'language', 'created_at', 'expires_at']
    list_filter = ['language', 'created_at']
    search_fields = ['query']
    readonly_fields = ['created_at']
