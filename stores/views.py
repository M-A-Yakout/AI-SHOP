"""
Store views
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Store
from .serializers import StoreSerializer, StoreCreateSerializer
from .permissions import IsStoreOwnerOrReadOnly


class StoreListView(generics.ListAPIView):
    """List all active stores"""
    queryset = Store.objects.filter(status='active')
    serializer_class = StoreSerializer
    filterset_fields = ['owner', 'status', 'city', 'country']
    search_fields = ['name', 'description']


class StoreCreateView(generics.CreateAPIView):
    """Create a new store"""
    serializer_class = StoreCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a store"""
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsStoreOwnerOrReadOnly]
    lookup_field = 'slug'


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_stores(request):
    """Get current user's stores"""
    stores = Store.objects.filter(owner=request.user)
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)
