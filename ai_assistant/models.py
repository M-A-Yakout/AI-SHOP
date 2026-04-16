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
