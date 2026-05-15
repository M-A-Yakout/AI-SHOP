"""
Main URL Configuration for AI Ecommerce Marketplace
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def api_root(request):
    """Root endpoint showing available API endpoints"""
    return JsonResponse({
        'message': 'Welcome to AI Ecommerce Marketplace API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api_documentation': '/api/docs/',
            'api_schema': '/api/schema/',
            'authentication': '/api/auth/',
            'stores': '/api/stores/',
            'products': '/api/products/',
            'orders': '/api/orders/',
            'ai_assistant': '/api/ai/',
            'news': '/api/news/',
        }
    })

urlpatterns = [
    # Root endpoint
    path('', api_root, name='api-root'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API Endpoints
    path('api/auth/', include('users.urls')),
    path('api/stores/', include('stores.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('api/news/', include('news.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "AI Ecommerce Marketplace Admin"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome to AI Ecommerce Marketplace"
