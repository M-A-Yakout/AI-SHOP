"""
AI Assistant URL patterns
"""
from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('product-assist/', views.product_assist, name='product_assist'),
    path('store-generator/', views.store_generator, name='store_generator'),
    path('usage-stats/', views.ai_usage_stats, name='usage_stats'),
    path('create-automated-store/', views.create_automated_store, name='create_automated_store'),
    path('search/', views.product_search_assistant, name='product_search'),  # Public endpoint
]
