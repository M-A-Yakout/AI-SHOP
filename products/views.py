"""
Product views
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Product, Category, Brand, ProductImage
from .serializers import (
    ProductSerializer, CategorySerializer, 
    BrandSerializer, ProductImageSerializer
)
from stores.permissions import IsStoreOwnerOrReadOnly


class ProductFilter(filters.FilterSet):
    """Custom filter for products to support store slug"""
    store = filters.NumberFilter(field_name='store__id')
    store_slug = filters.CharFilter(field_name='store__slug')
    category = filters.NumberFilter(field_name='category__id')
    category_slug = filters.CharFilter(field_name='category__slug')
    brand = filters.NumberFilter(field_name='brand__id')
    brand_slug = filters.CharFilter(field_name='brand__slug')
    
    class Meta:
        model = Product
        fields = ['store', 'store_slug', 'category', 'category_slug', 'brand', 'brand_slug', 'status', 'is_featured']


class ProductListView(generics.ListAPIView):
    """List all published products"""
    queryset = Product.objects.filter(status='published')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['price', 'created_at', 'name']


@api_view(['GET'])
@permission_classes([])
def search_products(request):
    """
    Search products using Django ORM with case-insensitive matching.
    
    Query parameters:
    - q: Search query (searches in name, description, tags, category)
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    - category: Category slug
    - limit: Number of results (default: 20, max: 100)
    
    Returns paginated JSON response with products from database.
    """
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_slug = request.GET.get('category')
    limit = min(int(request.GET.get('limit', 20)), 100)  # Max 100 results
    
    # Start with published products
    products = Product.objects.filter(status='published').select_related(
        'category', 'brand', 'store'
    )
    
    # Apply search query if provided
    if query:
        # Split query into keywords for better matching
        keywords = query.lower().split()
        q_objects = Q()
        
        for keyword in keywords:
            q_objects |= Q(name__icontains=keyword)
            q_objects |= Q(description__icontains=keyword)
            q_objects |= Q(short_description__icontains=keyword)
            q_objects |= Q(tags__icontains=keyword)
            q_objects |= Q(category__name__icontains=keyword)
            q_objects |= Q(brand__name__icontains=keyword)
        
        products = products.filter(q_objects).distinct()
    
    # Apply price filters
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Apply category filter
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Order by relevance (products with query in name first)
    if query:
        products = products.order_by('-is_featured', '-created_at')
    else:
        products = products.order_by('-is_featured', '-created_at')
    
    # Limit results
    total_count = products.count()
    products = products[:limit]
    
    # Serialize results
    serializer = ProductSerializer(products, many=True)
    
    return Response({
        'success': True,
        'query': query,
        'total_count': total_count,
        'returned_count': len(serializer.data),
        'products': serializer.data,
        'filters': {
            'min_price': min_price,
            'max_price': max_price,
            'category': category_slug,
            'limit': limit
        }
    }, status=status.HTTP_200_OK)


class ProductCreateView(generics.CreateAPIView):
    """Create a new product"""
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        store = serializer.validated_data['store']
        if store.owner != self.request.user:
            raise permissions.PermissionDenied("You can only add products to your own stores.")
        serializer.save()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def perform_update(self, serializer):
        product = self.get_object()
        if product.store.owner != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own products.")
        serializer.save()


class CategoryListView(generics.ListCreateAPIView):
    """List and create categories"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class BrandListView(generics.ListCreateAPIView):
    """List and create brands"""
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a brand"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
