"""
Product models for ecommerce marketplace
"""
from django.db import models
from django.utils.text import slugify
from stores.models import Store


class Category(models.Model):
    """Product category"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """Product brand"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Main product model"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('out_of_stock', 'Out of Stock'),
    )
    
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags")
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['store']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['name']),  # Index for search performance
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @classmethod
    def search(cls, query, filters=None):
        """
        Search products using Django ORM with case-insensitive matching.
        
        Args:
            query (str): Search query string
            filters (dict): Optional filters (category, min_price, max_price, etc.)
        
        Returns:
            QuerySet: Filtered products
        """
        from django.db.models import Q
        
        products = cls.objects.filter(status='published').select_related(
            'category', 'brand', 'store'
        )
        
        if query:
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
        
        # Apply additional filters if provided
        if filters:
            if 'min_price' in filters:
                products = products.filter(price__gte=filters['min_price'])
            if 'max_price' in filters:
                products = products.filter(price__lte=filters['max_price'])
            if 'category' in filters:
                products = products.filter(category__slug=filters['category'])
            if 'store' in filters:
                products = products.filter(store__slug=filters['store'])
        
        return products.order_by('-is_featured', '-created_at')


class ProductImage(models.Model):
    """Product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-is_primary']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"
