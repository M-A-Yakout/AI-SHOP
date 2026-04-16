"""
Product serializers
"""
from rest_framework import serializers
from .models import Product, Category, Brand, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    children_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'image', 
                 'is_active', 'children_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_children_count(self, obj):
        return obj.children.count()


class BrandSerializer(serializers.ModelSerializer):
    """Brand serializer"""
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'description', 'logo', 'website', 
                 'is_active', 'products_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_products_count(self, obj):
        return obj.products.count()


class ProductImageSerializer(serializers.ModelSerializer):
    """Product image serializer"""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer"""
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'store', 'store_name', 'category', 'category_name', 
            'brand', 'brand_name', 'name', 'slug', 'description', 
            'short_description', 'price', 'compare_price', 'cost_price',
            'sku', 'barcode', 'quantity', 'weight', 'status', 'is_featured',
            'tags', 'meta_title', 'meta_description', 'images',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
