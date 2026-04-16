"""
News serializers
"""
from rest_framework import serializers
from .models import NewsArticle


class NewsArticleSerializer(serializers.ModelSerializer):
    """News article serializer"""
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'author', 'author_name', 'title', 'slug', 'content',
            'excerpt', 'featured_image', 'status', 'tags', 'views_count',
            'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'views_count', 'created_at', 'updated_at']
