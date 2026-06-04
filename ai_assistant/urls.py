"""
AI Assistant URL patterns - Enhanced with conversations, recommendations & web search
"""
from django.urls import path
from . import views, enhanced_views

app_name = 'ai_assistant'

urlpatterns = [
    # Original endpoints
    path('product-assist/', views.product_assist, name='product_assist'),
    path('store-generator/', views.store_generator, name='store_generator'),
    path('usage-stats/', views.ai_usage_stats, name='usage_stats'),
    path('create-automated-store/', views.create_automated_store, name='create_automated_store'),
    path('search/', views.product_search_assistant, name='product_search'),  # Public endpoint
    
    # Enhanced conversation endpoints
    path('conversations/create/', enhanced_views.create_conversation, name='create_conversation'),
    path('conversations/<int:session_id>/send/', enhanced_views.send_message, name='send_message'),
    path('conversations/<int:session_id>/', enhanced_views.get_conversation, name='get_conversation'),
    path('conversations/', enhanced_views.list_conversations, name='list_conversations'),
    
    # Recommendations endpoints
    path('recommendations/', enhanced_views.get_recommendations, name='get_recommendations'),
    path('recommendations/<int:rec_id>/click/', enhanced_views.record_recommendation_click, name='record_click'),
    
    # Web search endpoints
    path('search/web/', enhanced_views.web_search, name='web_search'),
    
    # Language endpoints
    path('languages/', enhanced_views.supported_languages, name='supported_languages'),
    path('languages/detect/', enhanced_views.detect_and_translate, name='detect_translate'),
    
    # Enhanced product assist with language support
    path('product-assist/multilingual/', enhanced_views.product_assist_multilingual, name='product_assist_ml'),
    
    # Intent-based endpoints
    path('search-and-recommend/', views.search_and_recommend, name='search_and_recommend'),
    path('generate-product-names/', views.generate_product_names, name='generate_product_names'),
]

