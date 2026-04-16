"""
News URL patterns
"""
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsArticleListView.as_view(), name='article_list'),
    path('create/', views.NewsArticleCreateView.as_view(), name='article_create'),
    path('<slug:slug>/', views.NewsArticleDetailView.as_view(), name='article_detail'),
]
