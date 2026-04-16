"""
Full Automation Flow - Idea to Working Store
Transforms a simple idea into a complete ecommerce store
"""
import logging
from typing import Dict, Any, List
from django.db import transaction
from django.contrib.auth import get_user_model

from stores.models import Store
from products.models import Category, Brand, Product
from .services import AIService, AIServiceError

User = get_user_model()
logger = logging.getLogger(__name__)


class StoreAutomationError(Exception):
    """Custom exception for store automation errors"""
    pass


class StoreAutomation:
    """
    Automates the complete process of creating a store from an idea
    
    Flow:
    1. User provides idea (e.g., "sports clothing store")
    2. AI generates store structure
    3. Create store in database
    4. Create categories in database
    5. Create brand in database
    6. Create products in database
    7. Return working store URL
    """
    
    def __init__(self, user):
        """
        Initialize automation with user context
        
        Args:
            user: User object who will own the store
        """
        self.user = user
        self.ai_service = AIService()
        self.created_objects = {
            'store': None,
            'categories': [],
            'brand': None,
            'products': []
        }
    
    @transaction.atomic
    def create_store_from_idea(self, idea: str) -> Dict[str, Any]:
        """
        Complete automation: idea → working store
        
        Args:
            idea: Simple store concept (e.g., "organic coffee shop")
            
        Returns:
            Dictionary with:
            - store: Store object
            - categories: List of Category objects
            - brand: Brand object
            - products: List of Product objects
            - store_url: URL to access the store
            - summary: Summary of what was created
            
        Raises:
            StoreAutomationError: If automation fails
        """
        logger.info(f"Starting store automation for idea: '{idea}' by user {self.user.username}")
        
        try:
            # Step 1: Generate store structure with AI
            logger.info("Step 1: Generating store structure with AI...")
            ai_result = self._generate_store_structure(idea)
            
            # Step 2: Create store
            logger.info("Step 2: Creating store in database...")
            store = self._create_store(ai_result['store'])
            
            # Step 3: Create categories
            logger.info("Step 3: Creating categories...")
            categories = self._create_categories(ai_result['categories'])
            
            # Step 4: Create brand
            logger.info("Step 4: Creating brand...")
            brand = self._create_brand(idea)
            
            # Step 5: Create products
            logger.info("Step 5: Creating products...")
            products = self._create_products(
                store=store,
                categories=categories,
                brand=brand,
                products_data=ai_result['sample_products']
            )
            
            # Step 6: Generate result
            result = self._generate_result(store, categories, brand, products, ai_result)
            
            logger.info(f"Store automation completed successfully! Store ID: {store.id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Store automation failed: {e}", exc_info=True)
            raise StoreAutomationError(f"Failed to create store: {str(e)}")
    
    def _generate_store_structure(self, idea: str) -> Dict[str, Any]:
        """
        Use AI to generate complete store structure
        
        Returns:
            AI-generated structure with store, categories, and products
        """
        try:
            result = self.ai_service.store_generator(idea, user=self.user)
            
            # Validate AI response
            if not all(key in result for key in ['store', 'categories', 'sample_products']):
                raise StoreAutomationError("Invalid AI response structure")
            
            if not result['categories']:
                raise StoreAutomationError("AI did not generate any categories")
            
            if not result['sample_products']:
                raise StoreAutomationError("AI did not generate any products")
            
            return result
            
        except AIServiceError as e:
            raise StoreAutomationError(f"AI service error: {e}")
    
    def _create_store(self, store_data: Dict[str, str]) -> Store:
        """
        Create store in database with unique slug handling
        
        Args:
            store_data: Dictionary with name, description, tagline
            
        Returns:
            Created Store object
        """
        from django.utils.text import slugify
        
        try:
            base_slug = slugify(store_data['name'])
            slug = base_slug
            counter = 1
            
            # Find unique slug
            while Store.objects.filter(slug=slug).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
                logger.info(f"Slug '{base_slug}' exists, trying '{slug}'")
            
            store = Store.objects.create(
                owner=self.user,
                name=store_data['name'],
                slug=slug,  # Explicitly set unique slug
                description=store_data['description'],
                status='active',  # Automatically activate
                email=self.user.email,
                phone=self.user.phone if hasattr(self.user, 'phone') else None
            )
            
            self.created_objects['store'] = store
            logger.info(f"Store created: {store.name} (ID: {store.id}, Slug: {store.slug})")
            
            return store
            
        except Exception as e:
            raise StoreAutomationError(f"Failed to create store: {e}")
    
    def _create_categories(self, categories_data: List[Dict[str, str]]) -> List[Category]:
        """
        Create categories in database with unique slug handling
        
        Args:
            categories_data: List of dictionaries with name and description
            
        Returns:
            List of created Category objects
        """
        from django.utils.text import slugify
        
        categories = []
        
        try:
            for cat_data in categories_data:
                # Generate unique slug
                base_slug = slugify(cat_data['name'])
                slug = base_slug
                counter = 1
                
                # Check if category with this slug exists
                while Category.objects.filter(slug=slug).exists():
                    counter += 1
                    slug = f"{base_slug}-{counter}"
                    logger.info(f"Category slug '{base_slug}' exists, trying '{slug}'")
                
                # Create category with explicit slug
                category = Category.objects.create(
                    name=cat_data['name'],
                    slug=slug,
                    description=cat_data.get('description', ''),
                    is_active=True
                )
                
                categories.append(category)
                logger.info(f"Category created: {category.name} (Slug: {category.slug})")
            
            self.created_objects['categories'] = categories
            
            return categories
            
        except Exception as e:
            raise StoreAutomationError(f"Failed to create categories: {e}")
    
    def _create_brand(self, idea: str) -> Brand:
        """
        Create brand in database with unique slug handling
        
        Args:
            idea: Store idea to derive brand name
            
        Returns:
            Created Brand object
        """
        from django.utils.text import slugify
        
        try:
            # Generate brand name from idea
            brand_name = f"{idea.title()} Brand"
            
            # Generate unique slug
            base_slug = slugify(brand_name)
            slug = base_slug
            counter = 1
            
            while Brand.objects.filter(slug=slug).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
                logger.info(f"Brand slug '{base_slug}' exists, trying '{slug}'")
            
            # Create brand with explicit slug
            brand = Brand.objects.create(
                name=brand_name,
                slug=slug,
                description=f'Premium {idea} products',
                is_active=True
            )
            
            self.created_objects['brand'] = brand
            logger.info(f"Brand created: {brand.name} (Slug: {brand.slug})")
            
            return brand
            
        except Exception as e:
            raise StoreAutomationError(f"Failed to create brand: {e}")
    
    def _create_products(
        self,
        store: Store,
        categories: List[Category],
        brand: Brand,
        products_data: List[Dict[str, Any]]
    ) -> List[Product]:
        """
        Create products in database with unique slug handling
        
        Args:
            store: Store object
            categories: List of Category objects
            brand: Brand object
            products_data: List of product dictionaries
            
        Returns:
            List of created Product objects
        """
        from django.utils.text import slugify
        
        products = []
        category_map = {cat.name: cat for cat in categories}
        
        try:
            for idx, prod_data in enumerate(products_data):
                # Find matching category
                category_name = prod_data.get('category', '')
                category = category_map.get(category_name)
                
                # If no match, use first category
                if not category and categories:
                    category = categories[0]
                
                # Generate unique slug
                base_slug = slugify(prod_data['name'])
                slug = base_slug
                counter = 1
                
                while Product.objects.filter(slug=slug).exists():
                    counter += 1
                    slug = f"{base_slug}-{counter}"
                    logger.info(f"Slug '{base_slug}' exists, trying '{slug}'")
                
                # Create product with explicit slug
                product = Product.objects.create(
                    store=store,
                    category=category,
                    brand=brand,
                    name=prod_data['name'],
                    slug=slug,  # Explicitly set unique slug
                    description=prod_data.get('description', ''),
                    short_description=prod_data.get('description', '')[:150],
                    price=prod_data.get('price', 0),
                    compare_price=prod_data.get('price', 0) * 1.3,  # 30% markup
                    quantity=100,  # Default stock
                    status='published',  # Auto-publish
                    is_featured=(idx == 0),  # First product is featured
                    tags=f"{store.name}, {category.name if category else ''}, {brand.name}",
                    sku=f"AUTO-{store.id}-{idx+1:03d}",
                    meta_title=f"Buy {prod_data['name']} Online",
                    meta_description=f"Shop {prod_data['name']} at {store.name}. {prod_data.get('description', '')[:100]}"
                )
                
                products.append(product)
                logger.info(f"Product created: {product.name} (ID: {product.id}, Slug: {product.slug})")
            
            self.created_objects['products'] = products
            
            return products
            
        except Exception as e:
            raise StoreAutomationError(f"Failed to create products: {e}")
    
    def _generate_result(
        self,
        store: Store,
        categories: List[Category],
        brand: Brand,
        products: List[Product],
        ai_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate final result with all created objects and URLs
        
        Returns:
            Complete result dictionary
        """
        from django.conf import settings
        
        # Generate store URL
        base_url = "http://localhost:8000" if settings.DEBUG else settings.ALLOWED_HOSTS[0]
        store_url = f"{base_url}/api/stores/{store.slug}/"
        
        return {
            'success': True,
            'message': f'Store "{store.name}" created successfully!',
            'store': {
                'id': store.id,
                'name': store.name,
                'slug': store.slug,
                'description': store.description,
                'status': store.status,
                'url': store_url,
                'api_url': store_url,
                'products_count': len(products)
            },
            'categories': [
                {
                    'id': cat.id,
                    'name': cat.name,
                    'slug': cat.slug,
                    'description': cat.description
                }
                for cat in categories
            ],
            'brand': {
                'id': brand.id,
                'name': brand.name,
                'slug': brand.slug
            },
            'products': [
                {
                    'id': prod.id,
                    'name': prod.name,
                    'slug': prod.slug,
                    'price': str(prod.price),
                    'category': prod.category.name if prod.category else None,
                    'status': prod.status,
                    'url': f"{base_url}/api/products/{prod.slug}/"
                }
                for prod in products
            ],
            'summary': {
                'total_categories': len(categories),
                'total_products': len(products),
                'ai_mode': ai_result.get('mode', 'unknown'),
                'tokens_used': ai_result.get('tokens_used', 0),
                'processing_time': ai_result.get('processing_time', 0)
            },
            'next_steps': [
                f"View your store: {store_url}",
                f"Add more products: POST /api/products/create/",
                f"Manage store: PUT {store_url}",
                f"View products: GET /api/products/?store={store.id}"
            ]
        }


def create_automated_store(user, idea: str) -> Dict[str, Any]:
    """
    Convenience function to create a store from an idea
    
    Args:
        user: User object
        idea: Store concept
        
    Returns:
        Result dictionary with created store and objects
        
    Example:
        result = create_automated_store(user, "organic coffee shop")
        print(f"Store created: {result['store']['url']}")
    """
    automation = StoreAutomation(user)
    return automation.create_store_from_idea(idea)
