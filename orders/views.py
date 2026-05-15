"""
Order views
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderListView(generics.ListAPIView):
    """List user's orders - both as customer and as seller"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Use Q objects to combine queries properly
        return Order.objects.filter(
            Q(customer=user) | Q(items__product__store__owner=user)
        ).distinct().order_by('-created_at')


class OrderCreateView(generics.CreateAPIView):
    """Create a new order - allows guest checkout"""
    serializer_class = OrderCreateSerializer
    permission_classes = []  # Allow anyone to create orders


class OrderDetailView(generics.RetrieveUpdateAPIView):
    """Get or update order details"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Allow access to orders where user is customer or seller
        return Order.objects.filter(
            Q(customer=user) | Q(items__product__store__owner=user)
        ).distinct()
