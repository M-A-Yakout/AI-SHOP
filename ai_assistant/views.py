"""
AI Assistant views with comprehensive error handling
"""
import logging
from django.db import models
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from .services import AIService, AIServiceError
from .automation import StoreAutomation, StoreAutomationError
from .serializers import (
    ProductAssistRequestSerializer,
    ProductAssistResponseSerializer,
    StoreGeneratorRequestSerializer,
    StoreGeneratorResponseSerializer,
    AIUsageStatsSerializer,
    ErrorResponseSerializer,
    AutomatedStoreRequestSerializer,
    AutomatedStoreResponseSerializer
)

logger = logging.getLogger(__name__)


@extend_schema(
    request=ProductAssistRequestSerializer,
    responses={
        200: ProductAssistResponseSerializer,
        400: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    examples=[
        OpenApiExample(
            'Product Assist Request',
            value={
                'name': 'Wireless Bluetooth Headphones',
                'description': 'High quality headphones with noise cancellation',
                'category': 'Electronics',
                'price': '79.99'
            },
            request_only=True,
        ),
        OpenApiExample(
            'Product Assist Response',
            value={
                'improved_title': 'Premium Wireless Bluetooth Headphones - Noise Cancelling',
                'seo_description': 'Experience superior sound quality with our Premium Wireless Bluetooth Headphones...',
                'category_suggestions': ['Electronics', 'Audio', 'Headphones', 'Wireless Accessories'],
                'tags': ['wireless', 'bluetooth', 'noise-cancelling', 'premium', 'audio'],
                'meta_title': 'Buy Premium Wireless Headphones | Noise Cancelling',
                'meta_description': 'Shop premium wireless Bluetooth headphones with noise cancellation...',
                'tokens_used': 245,
                'mode': 'openai',
                'processing_time': 1.23
            },
            response_only=True,
        ),
    ],
    tags=['AI Assistant'],
    description='Enhance product information using AI. Provides improved title, SEO description, category suggestions, and tags.'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_assist(request):
    """
    AI-powered product enhancement
    
    Takes product draft input and returns:
    - Improved, SEO-friendly title
    - Compelling product description
    - Category suggestions
    - Relevant tags
    - Meta title and description for SEO
    
    Automatically falls back to mock mode if OpenAI API is unavailable.
    """
    # Validate input
    serializer = ProductAssistRequestSerializer(data=request.data)
    if not serializer.is_valid():
        logger.warning(f"Invalid product assist request: {serializer.errors}")
        return Response(
            {
                'error': 'Invalid input',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Call AI service
        ai_service = AIService()
        result = ai_service.product_assist(
            product_data=serializer.validated_data,
            user=request.user
        )
        
        # Add success indicator
        result['success'] = True
        
        # Log success
        logger.info(f"Product assist successful for user {request.user.username}. Mode: {result.get('mode', 'unknown')}")
        
        return Response(result, status=status.HTTP_200_OK)
        
    except AIServiceError as e:
        logger.error(f"AI Service error in product_assist: {e}")
        return Response(
            {
                'error': 'AI service error',
                'message': str(e),
                'success': False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        logger.error(f"Unexpected error in product_assist: {e}", exc_info=True)
        return Response(
            {
                'error': 'Internal server error',
                'message': 'An unexpected error occurred. Please try again later.',
                'success': False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    request=StoreGeneratorRequestSerializer,
    responses={
        200: StoreGeneratorResponseSerializer,
        400: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    examples=[
        OpenApiExample(
            'Store Generator Request',
            value={'idea': 'organic skincare products'},
            request_only=True,
        ),
        OpenApiExample(
            'Store Generator Response',
            value={
                'store': {
                    'name': 'Organic Skincare Store',
                    'description': 'Your trusted source for natural, organic skincare products...',
                    'tagline': 'Natural beauty, naturally'
                },
                'categories': [
                    {'name': 'Cleansers', 'description': 'Gentle organic face and body cleansers'},
                    {'name': 'Moisturizers', 'description': 'Hydrating organic creams and lotions'}
                ],
                'sample_products': [
                    {
                        'name': 'Organic Rose Water Toner',
                        'description': 'Pure rose water toner for all skin types',
                        'price': 24.99,
                        'category': 'Toners'
                    }
                ],
                'tokens_used': 450,
                'mode': 'openai',
                'processing_time': 2.15
            },
            response_only=True,
        ),
    ],
    tags=['AI Assistant'],
    description='Generate complete store structure from a simple idea. Returns store details, categories, and sample products.'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_generator(request):
    """
    AI-powered store generation from user idea
    
    Takes a store concept/idea and returns:
    - Store name, description, and tagline
    - Relevant product categories
    - Sample products with pricing
    
    Automatically falls back to mock mode if OpenAI API is unavailable.
    """
    # Validate input
    serializer = StoreGeneratorRequestSerializer(data=request.data)
    if not serializer.is_valid():
        logger.warning(f"Invalid store generator request: {serializer.errors}")
        return Response(
            {
                'error': 'Invalid input',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Call AI service
        ai_service = AIService()
        result = ai_service.store_generator(
            store_idea=serializer.validated_data['idea'],
            user=request.user
        )
        
        # Add success indicator
        result['success'] = True
        
        # Log success
        logger.info(f"Store generator successful for user {request.user.username}. Mode: {result.get('mode', 'unknown')}")
        
        return Response(result, status=status.HTTP_200_OK)
        
    except AIServiceError as e:
        logger.error(f"AI Service error in store_generator: {e}")
        return Response(
            {
                'error': 'AI service error',
                'message': str(e),
                'success': False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        logger.error(f"Unexpected error in store_generator: {e}", exc_info=True)
        return Response(
            {
                'error': 'Internal server error',
                'message': 'An unexpected error occurred. Please try again later.',
                'success': False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    responses={
        200: AIUsageStatsSerializer,
        500: ErrorResponseSerializer,
    },
    tags=['AI Assistant'],
    description='Get AI usage statistics for the current user including request counts and token usage.'
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ai_usage_stats(request):
    """
    Get AI usage statistics for current user
    
    Returns:
    - Total requests count
    - Requests by type
    - Total tokens used
    - Average processing time
    """
    try:
        from .models import AIRequest
        
        requests_qs = AIRequest.objects.filter(user=request.user)
        
        stats = {
            'total_requests': requests_qs.count(),
            'product_assist_count': requests_qs.filter(request_type='product_assist').count(),
            'store_generator_count': requests_qs.filter(request_type='store_generator').count(),
            'total_tokens_used': sum(r.tokens_used for r in requests_qs),
            'avg_processing_time': round(
                sum(r.processing_time for r in requests_qs) / requests_qs.count(), 2
            ) if requests_qs.count() > 0 else 0,
            'success': True
        }
        
        logger.info(f"AI usage stats retrieved for user {request.user.username}")
        
        return Response(stats, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving AI usage stats: {e}", exc_info=True)
        return Response(
            {
                'error': 'Failed to retrieve statistics',
                'message': str(e),
                'success': False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@extend_schema(
    request=AutomatedStoreRequestSerializer,
    responses={
        201: AutomatedStoreResponseSerializer,
        400: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    examples=[
        OpenApiExample(
            'Automated Store Request',
            value={'idea': 'sports clothing store'},
            request_only=True,
        ),
        OpenApiExample(
            'Automated Store Response',
            value={
                'success': True,
                'message': 'Store "Sports Clothing Store" created successfully!',
                'store': {
                    'id': 1,
                    'name': 'Sports Clothing Store',
                    'slug': 'sports-clothing-store',
                    'description': 'Your one-stop shop for all sports clothing needs...',
                    'status': 'active',
                    'url': 'http://localhost:8000/api/stores/sports-clothing-store/',
                    'products_count': 8
                },
                'categories': [
                    {'id': 1, 'name': 'Athletic Wear', 'slug': 'athletic-wear'},
                    {'id': 2, 'name': 'Running Gear', 'slug': 'running-gear'}
                ],
                'brand': {
                    'id': 1,
                    'name': 'Sports Clothing Brand',
                    'slug': 'sports-clothing-brand'
                },
                'products': [
                    {
                        'id': 1,
                        'name': 'Professional Running Shoes',
                        'slug': 'professional-running-shoes',
                        'price': '129.99',
                        'category': 'Running Gear',
                        'status': 'published'
                    }
                ],
                'summary': {
                    'total_categories': 4,
                    'total_products': 8,
                    'ai_mode': 'mock',
                    'tokens_used': 0,
                    'processing_time': 0.5
                },
                'next_steps': [
                    'View your store: http://localhost:8000/api/stores/sports-clothing-store/',
                    'Add more products: POST /api/products/create/',
                    'Manage store: PUT http://localhost:8000/api/stores/sports-clothing-store/'
                ]
            },
            response_only=True,
        ),
    ],
    tags=['AI Assistant - Automation'],
    description='🚀 FULL AUTOMATION: Transform a simple idea into a complete working ecommerce store with categories and products. This endpoint creates everything automatically!'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_automated_store(request):
    """
    🚀 FULL AUTOMATION: Idea → Working Store
    
    This endpoint automates the complete process:
    1. Takes a simple idea (e.g., "sports clothing store")
    2. Uses AI to generate store structure
    3. Creates store in database
    4. Creates categories automatically
    5. Creates brand automatically
    6. Generates and creates sample products
    7. Returns working store URL
    
    Result: A fully functional ecommerce store ready to use!
    
    Example ideas:
    - "organic coffee shop"
    - "vintage books store"
    - "handmade jewelry"
    - "sports equipment"
    - "pet supplies"
    """
    # Validate input
    serializer = AutomatedStoreRequestSerializer(data=request.data)
    if not serializer.is_valid():
        logger.warning(f"Invalid automated store request: {serializer.errors}")
        return Response(
            {
                'error': 'Invalid input',
                'details': serializer.errors,
                'success': False
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    idea = serializer.validated_data['idea']
    
    try:
        # Create automation instance
        automation = StoreAutomation(user=request.user)
        
        # Run full automation
        logger.info(f"Starting automated store creation for: '{idea}' by user {request.user.username}")
        result = automation.create_store_from_idea(idea)
        
        logger.info(f"Automated store creation successful! Store: {result['store']['name']}")
        
        return Response(result, status=status.HTTP_201_CREATED)
        
    except StoreAutomationError as e:
        logger.error(f"Store automation error: {e}")
        return Response(
            {
                'error': 'Store automation failed',
                'message': str(e),
                'success': False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        logger.error(f"Unexpected error in automated store creation: {e}", exc_info=True)
        return Response(
            {
                'error': 'Internal server error',
                'message': 'An unexpected error occurred during store creation. Please try again later.',
                'success': False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    tags=['AI Assistant - Public'],
    description='🛍️ AI Shopping Assistant: Search for products using natural language. No authentication required!'
)
@api_view(['POST'])
@permission_classes([])  # Allow any user (no authentication required)
def product_search_assistant(request):
    """
    🛍️ AI Shopping Assistant for Customers
    
    Searches products directly from database using Django ORM.
    The AI provides helpful responses based on the search results.
    
    Example queries:
    - "I need running shoes under $100"
    - "Looking for organic coffee"
    - "Show me wireless headphones"
    - "What sports equipment do you have?"
    
    Returns:
    - AI response explaining the products
    - List of matching products from database
    - Suggestions and recommendations
    """
    from products.models import Product
    from products.serializers import ProductSerializer
    from django.db.models import Q
    
    query = request.data.get('query', '').strip()
    
    if not query:
        return Response(
            {
                'error': 'Query is required',
                'success': False
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Extract keywords from query for better search
        keywords = query.lower().split()
        
        # Build dynamic query using Q objects for OR conditions
        q_objects = Q()
        for keyword in keywords:
            q_objects |= Q(name__icontains=keyword)
            q_objects |= Q(description__icontains=keyword)
            q_objects |= Q(short_description__icontains=keyword)
            q_objects |= Q(tags__icontains=keyword)
            q_objects |= Q(category__name__icontains=keyword)
        
        # Search for products using Django ORM with case-insensitive matching
        products = Product.objects.filter(
            q_objects,
            status='published'
        ).select_related('category', 'brand', 'store').distinct()[:20]  # Limit to 20 results
        
        products_count = products.count()
        
        # Prepare AI context from database results
        products_context = []
        for p in products[:5]:  # Use top 5 for AI context
            products_context.append({
                'name': p.name,
                'price': float(p.price),
                'description': p.short_description or p.description[:150] if p.description else '',
                'category': p.category.name if p.category else 'Uncategorized'
            })
        
        # Generate AI response
        ai_service = AIService()
        
        if ai_service.mock_mode or not ai_service.client:
            # Mock response
            if products_count > 0:
                product_names = [p.name for p in products[:3]]
                ai_response = f"I found {products_count} product{'s' if products_count != 1 else ''} matching '{query}'. "
                ai_response += f"Here are some great options: {', '.join(product_names)}. "
                ai_response += "All products are high quality and available for immediate purchase."
            else:
                ai_response = f"I couldn't find any products matching '{query}'. "
                ai_response += "Try searching with different keywords or browse our categories to discover more products."
        else:
            # Use OpenAI for better responses
            try:
                prompt = f"""You are a helpful shopping assistant. A customer asked: "{query}"

I found {products_count} products in our database.

Top products:
{chr(10).join([f"- {p['name']} (${p['price']}) - {p['description']}" for p in products_context])}

Provide a friendly, helpful response (2-3 sentences) recommending the best products for their needs."""
                
                response = ai_service.client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role': 'system', 'content': 'You are a friendly shopping assistant helping customers find products.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                
                ai_response = response.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenAI error in product search: {e}")
                ai_response = f"I found {products_count} product{'s' if products_count != 1 else ''} for you. Check them out below!"
        
        # Serialize products from database
        serializer = ProductSerializer(products, many=True)
        
        # Prepare suggestions based on results
        suggestions = []
        if products_count == 0:
            suggestions = [
                'Try using more general terms',
                'Browse by category',
                'Check our featured products',
                'Search for related items'
            ]
        
        return Response({
            'success': True,
            'query': query,
            'ai_response': ai_response,
            'products_count': products_count,
            'products': serializer.data,
            'suggestions': suggestions
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error in product search assistant: {e}", exc_info=True)
        return Response(
            {
                'error': 'Search failed',
                'message': str(e),
                'success': False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
