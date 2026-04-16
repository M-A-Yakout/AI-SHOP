"""
Order views
"""
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderListView(generics.ListAPIView):
    """List user's orders"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    """Create a new order"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        import uuid
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        serializer.save(customer=self.request.user, order_number=order_number)


class OrderDetailView(generics.RetrieveAPIView):
    """Get order details"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
