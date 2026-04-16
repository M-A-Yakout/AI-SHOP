"""
Store URL patterns
"""
from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.StoreListView.as_view(), name='store_list'),
    path('create/', views.StoreCreateView.as_view(), name='store_create'),
    path('my-stores/', views.my_stores, name='my_stores'),
    path('<slug:slug>/', views.StoreDetailView.as_view(), name='store_detail'),
]
