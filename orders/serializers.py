"""
Order serializers
"""
from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer"""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'subtotal']
        read_only_fields = ['id', 'subtotal']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Order item creation serializer"""
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer"""
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'customer_name', 'status',
            'payment_status', 'total_amount', 'shipping_address', 
            'billing_address', 'phone', 'email', 'notes', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Order creation serializer with items"""
    items = OrderItemCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = [
            'shipping_address', 'billing_address', 'phone', 
            'email', 'notes', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate total amount
        total_amount = 0
        order_items = []
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Check stock
            if product.quantity < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}. Only {product.quantity} available."
                )
            
            subtotal = product.price * quantity
            total_amount += subtotal
            
            order_items.append({
                'product': product,
                'product_name': product.name,
                'product_price': product.price,
                'quantity': quantity,
                'subtotal': subtotal
            })
        
        # Create order
        import uuid
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Get customer from context (will be None for guest checkout)
        customer = self.context['request'].user if self.context['request'].user.is_authenticated else None
        
        order = Order.objects.create(
            order_number=order_number,
            customer=customer,
            total_amount=total_amount,
            **validated_data
        )
        
        # Create order items and update stock
        for item_data in order_items:
            OrderItem.objects.create(order=order, **item_data)
            product = item_data['product']
            product.quantity -= item_data['quantity']
            product.save()
        
        return order
    
    def to_representation(self, instance):
        # Return full order details using OrderSerializer
        return OrderSerializer(instance, context=self.context).data
