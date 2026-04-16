"""
News views
"""
from rest_framework import generics, permissions
from .models import NewsArticle
from .serializers import NewsArticleSerializer


class NewsArticleListView(generics.ListAPIView):
    """List all published articles"""
    queryset = NewsArticle.objects.filter(status='published')
    serializer_class = NewsArticleSerializer
    search_fields = ['title', 'content', 'tags']


class NewsArticleCreateView(generics.CreateAPIView):
    """Create a new article"""
    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete an article"""
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)
