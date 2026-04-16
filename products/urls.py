"""
Product URL patterns
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Categories (must come before product detail to avoid slug conflict)
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Brands (must come before product detail to avoid slug conflict)
    path('brands/', views.BrandListView.as_view(), name='brand_list'),
    path('brands/<slug:slug>/', views.BrandDetailView.as_view(), name='brand_detail'),
    
    # Search endpoint
    path('search/', views.search_products, name='product_search'),
    
    # Products
    path('', views.ProductListView.as_view(), name='product_list'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
