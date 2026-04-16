"""
Store serializers
"""
from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    """Store serializer"""
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    products_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Store
        fields = [
            'id', 'owner', 'owner_name', 'name', 'slug', 'description',
            'logo', 'banner', 'status', 'email', 'phone', 'address',
            'city', 'country', 'postal_code', 'website', 'products_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        if Store.objects.filter(name__iexact=value).exists():
            if self.instance and self.instance.name.lower() == value.lower():
                return value
            raise serializers.ValidationError("A store with this name already exists.")
        return value


class StoreCreateSerializer(serializers.ModelSerializer):
    """Store creation serializer"""
    
    class Meta:
        model = Store
        fields = ['name', 'description', 'logo', 'banner', 'email', 'phone', 
                 'address', 'city', 'country', 'postal_code', 'website']
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
