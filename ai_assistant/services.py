"""
AI Service Layer - OpenAI Integration
Enhanced with proper error handling and modern OpenAI API
"""
import json
import time
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from .models import AIRequest

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Custom exception for AI service errors"""
    pass


class AIService:
    """
    AI Service for product and store generation
    Supports both OpenAI API and mock mode with automatic fallback
    """
    
    def __init__(self):
        self.mock_mode = settings.AI_MOCK_MODE
        self.client = None
        
        # Try to initialize OpenAI client if not in mock mode
        if not self.mock_mode and settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized successfully")
            except ImportError as e:
                logger.warning(f"OpenAI package not available: {e}. Falling back to mock mode.")
                self.mock_mode = True
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}. Falling back to mock mode.")
                self.mock_mode = True
        else:
            logger.info("Running in mock mode (no API key or AI_MOCK_MODE=True)")
            self.mock_mode = True
    
    def product_assist(self, product_data: Dict[str, Any], user=None) -> Dict[str, Any]:
        """
        Enhance product information using AI
        
        Args:
            product_data: Dictionary with keys: name, description, category, price
            user: Optional user object for logging
            
        Returns:
            Dictionary with enhanced product information
            
        Raises:
            AIServiceError: If both API and fallback fail
        """
        start_time = time.time()
        
        try:
            if self.mock_mode or not self.client:
                logger.info("Using mock product assist")
                result = self._mock_product_assist(product_data)
            else:
                logger.info("Using OpenAI API for product assist")
                result = self._openai_product_assist(product_data)
        except Exception as e:
            logger.error(f"Error in product_assist: {e}")
            # Fallback to mock if OpenAI fails
            logger.info("Falling back to mock mode due to error")
            result = self._mock_product_assist(product_data)
            result['fallback_used'] = True
            result['error_message'] = str(e)
        
        processing_time = time.time() - start_time
        result['processing_time'] = round(processing_time, 2)
        
        # Log request to database
        if user:
            try:
                AIRequest.objects.create(
                    user=user,
                    request_type='product_assist',
                    input_data=product_data,
                    output_data=result,
                    tokens_used=result.get('tokens_used', 0),
                    processing_time=processing_time
                )
            except Exception as e:
                logger.error(f"Failed to log AI request: {e}")
        
        return result
    
    def store_generator(self, store_idea: str, user=None) -> Dict[str, Any]:
        """
        Generate complete store structure from user idea
        
        Args:
            store_idea: Store concept or idea string
            user: Optional user object for logging
            
        Returns:
            Dictionary with store structure, categories, and sample products
            
        Raises:
            AIServiceError: If both API and fallback fail
        """
        start_time = time.time()
        
        try:
            if self.mock_mode or not self.client:
                logger.info("Using mock store generator")
                result = self._mock_store_generator(store_idea)
            else:
                logger.info("Using OpenAI API for store generation")
                result = self._openai_store_generator(store_idea)
        except Exception as e:
            logger.error(f"Error in store_generator: {e}")
            # Fallback to mock if OpenAI fails
            logger.info("Falling back to mock mode due to error")
            result = self._mock_store_generator(store_idea)
            result['fallback_used'] = True
            result['error_message'] = str(e)
        
        processing_time = time.time() - start_time
        result['processing_time'] = round(processing_time, 2)
        
        # Log request to database
        if user:
            try:
                AIRequest.objects.create(
                    user=user,
                    request_type='store_generator',
                    input_data={'idea': store_idea},
                    output_data=result,
                    tokens_used=result.get('tokens_used', 0),
                    processing_time=processing_time
                )
            except Exception as e:
                logger.error(f"Failed to log AI request: {e}")
        
        return result
    
    def _mock_product_assist(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock AI response for product assistance
        Used when OpenAI API is not available or as fallback
        """
        name = product_data.get('name', 'Product')
        description = product_data.get('description', '')
        category = product_data.get('category', '')
        
        # Generate smart mock data based on input
        improved_title = f"Premium {name} - High Quality"
        
        # Create description
        if description:
            seo_description = f"Discover our {name}. {description[:100]}... Perfect for your needs with excellent quality and value."
        else:
            seo_description = f"Shop {name} online. Premium quality, competitive prices, and fast shipping. Order now!"
        
        # Smart category suggestions based on input
        category_suggestions = []
        if category:
            category_suggestions.append(category)
        
        # Add generic categories
        category_suggestions.extend(['Electronics', 'Accessories', 'Home & Garden'])
        category_suggestions = list(set(category_suggestions))[:5]  # Remove duplicates, max 5
        
        # Generate tags from name and description
        tags = ['premium', 'quality', 'bestseller', 'trending']
        name_words = name.lower().split()
        tags.extend([word for word in name_words if len(word) > 3][:4])
        tags = list(set(tags))[:8]  # Remove duplicates, max 8
        
        return {
            'improved_title': improved_title,
            'seo_description': seo_description,
            'category_suggestions': category_suggestions,
            'tags': tags,
            'meta_title': f"Buy {name} Online | Best Deals & Fast Shipping",
            'meta_description': seo_description[:160],  # SEO limit
            'tokens_used': 0,
            'mode': 'mock'
        }
    
    def _openai_product_assist(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use OpenAI API for product assistance
        
        Raises:
            AIServiceError: If API call fails
        """
        if not self.client:
            raise AIServiceError("OpenAI client not initialized")
        
        name = product_data.get('name', '')
        description = product_data.get('description', '')
        category = product_data.get('category', '')
        price = product_data.get('price', '')
        
        # Construct detailed prompt
        prompt = f"""You are an ecommerce product optimization expert. Enhance this product information:

Product Name: {name}
Description: {description}
Category: {category}
Price: ${price}

Please provide:
1. An improved, SEO-friendly product title (max 100 characters)
2. A compelling product description (100-150 words) that highlights benefits
3. 3-5 relevant category suggestions
4. 5-8 relevant product tags (single words or short phrases)
5. Meta title for SEO (max 60 characters)
6. Meta description for SEO (max 160 characters)

Return ONLY a valid JSON object with these exact keys:
{{
    "improved_title": "...",
    "seo_description": "...",
    "category_suggestions": ["...", "..."],
    "tags": ["...", "..."],
    "meta_title": "...",
    "meta_description": "..."
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ecommerce product optimizer. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800,
                response_format={"type": "json_object"}  # Ensure JSON response
            )
            
            # Parse response
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # Add metadata
            result['tokens_used'] = response.usage.total_tokens
            result['mode'] = 'openai'
            
            logger.info(f"OpenAI API call successful. Tokens used: {result['tokens_used']}")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            raise AIServiceError(f"Invalid JSON response from OpenAI: {e}")
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise AIServiceError(f"OpenAI API error: {e}")
    
    def _mock_store_generator(self, store_idea: str) -> Dict[str, Any]:
        """
        Mock AI response for store generation
        Used when OpenAI API is not available or as fallback
        """
        idea_title = store_idea.title()
        
        return {
            'store': {
                'name': f"{idea_title} Store",
                'description': f"Your one-stop shop for all {store_idea} needs. Quality products at competitive prices with fast shipping.",
                'tagline': f"Best {store_idea} marketplace online"
            },
            'categories': [
                {
                    'name': f'{idea_title} Essentials',
                    'description': f'Core {store_idea} products for everyday use'
                },
                {
                    'name': f'{idea_title} Premium',
                    'description': f'High-end {store_idea} selection for professionals'
                },
                {
                    'name': f'{idea_title} Accessories',
                    'description': f'Complementary items and add-ons'
                },
                {
                    'name': f'{idea_title} Bundles',
                    'description': f'Value packages and combo deals'
                }
            ],
            'sample_products': [
                {
                    'name': f'Professional {idea_title} Kit',
                    'description': f'Complete professional-grade {store_idea} kit with all essentials included',
                    'price': 99.99,
                    'category': f'{idea_title} Premium'
                },
                {
                    'name': f'Starter {idea_title} Pack',
                    'description': f'Perfect starter pack for beginners in {store_idea}',
                    'price': 49.99,
                    'category': f'{idea_title} Essentials'
                },
                {
                    'name': f'{idea_title} Accessories Set',
                    'description': f'Essential accessories to enhance your {store_idea} experience',
                    'price': 29.99,
                    'category': f'{idea_title} Accessories'
                }
            ],
            'tokens_used': 0,
            'mode': 'mock'
        }
    
    def _openai_store_generator(self, store_idea: str) -> Dict[str, Any]:
        """
        Use OpenAI API for store generation
        
        Raises:
            AIServiceError: If API call fails
        """
        if not self.client:
            raise AIServiceError("OpenAI client not initialized")
        
        prompt = f"""You are an ecommerce business consultant. Generate a complete store structure for: "{store_idea}"

Please provide:
1. Store name, description (2-3 sentences), and tagline
2. 4-6 relevant product categories with descriptions
3. 5-10 sample products with names, descriptions, and suggested prices

Return ONLY a valid JSON object with this exact structure:
{{
    "store": {{
        "name": "...",
        "description": "...",
        "tagline": "..."
    }},
    "categories": [
        {{"name": "...", "description": "..."}},
        ...
    ],
    "sample_products": [
        {{"name": "...", "description": "...", "price": 0.0, "category": "..."}},
        ...
    ]
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ecommerce business consultant. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # Add metadata
            result['tokens_used'] = response.usage.total_tokens
            result['mode'] = 'openai'
            
            logger.info(f"OpenAI API call successful. Tokens used: {result['tokens_used']}")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            raise AIServiceError(f"Invalid JSON response from OpenAI: {e}")
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise AIServiceError(f"OpenAI API error: {e}")
