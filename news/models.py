"""
News/Blog models
"""
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class NewsArticle(models.Model):
    """News/Blog article model"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True, null=True)
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    tags = models.CharField(max_length=500, blank=True, null=True)
    views_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
