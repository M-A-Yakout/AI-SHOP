"""
AI Assistant models for tracking AI interactions
"""
from django.db import models
from django.conf import settings


class AIRequest(models.Model):
    """Track AI API requests for analytics"""
    REQUEST_TYPE_CHOICES = (
        ('product_assist', 'Product Assistance'),
        ('store_generator', 'Store Generator'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_requests')
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE_CHOICES)
    input_data = models.JSONField()
    output_data = models.JSONField()
    tokens_used = models.IntegerField(default=0)
    processing_time = models.FloatField(help_text="Processing time in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.request_type} - {self.user.username} - {self.created_at}"


class ConversationSession(models.Model):
    """Track AI conversation sessions for context and history"""
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('ar', 'Arabic'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('zh', 'Chinese'),
        ('ja', 'Japanese'),
        ('pt', 'Portuguese'),
        ('ru', 'Russian'),
        ('hi', 'Hindi'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_conversations')
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    title = models.CharField(max_length=255, blank=True)
    context = models.JSONField(default=dict, help_text="Conversation context and metadata")
    message_count = models.IntegerField(default=0)
    tokens_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title or 'Session'} - {self.user.username} ({self.language})"


class ConversationMessage(models.Model):
    """Store individual messages in a conversation"""
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    )
    
    session = models.ForeignKey(ConversationSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    original_language = models.CharField(max_length=5, blank=True)
    translated_content = models.JSONField(default=dict, help_text="Translations in other languages")
    metadata = models.JSONField(default=dict, help_text="Additional message metadata (sources, references, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class AIRecommendation(models.Model):
    """Store AI-generated recommendations for users"""
    RECOMMENDATION_TYPE_CHOICES = (
        ('product', 'Product Recommendation'),
        ('store', 'Store Recommendation'),
        ('category', 'Category Suggestion'),
        ('deal', 'Special Deal'),
        ('trending', 'Trending Item'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=50, choices=RECOMMENDATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    language = models.CharField(max_length=5, default='en')
    reason = models.TextField(help_text="Why this recommendation was made")
    data = models.JSONField(default=dict, help_text="Product/store data or link references")
    confidence_score = models.FloatField(default=0.0, help_text="Confidence of recommendation (0-1)")
    clicked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recommendation_type}: {self.title}"


class WebSearchCache(models.Model):
    """Cache web search results to improve performance"""
    query = models.CharField(max_length=500, unique=True)
    language = models.CharField(max_length=5, default='en')
    results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="When this cache expires")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['query', 'language']),
        ]
    
    def __str__(self):
        return f"Search: {self.query}"
