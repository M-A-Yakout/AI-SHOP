"""
Installation Verification Script
Run this after setup to verify everything is working correctly
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from stores.models import Store
from products.models import Product, Category, Brand
from orders.models import Order
from news.models import NewsArticle
from ai_assistant.models import AIRequest

User = get_user_model()

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def print_info(text):
    print(f"  {text}")

def verify_models():
    """Verify all models are accessible"""
    print_header("Verifying Models")
    
    try:
        models = [
            ('User', User),
            ('Store', Store),
            ('Product', Product),
            ('Category', Category),
            ('Brand', Brand),
            ('Order', Order),
            ('NewsArticle', NewsArticle),
            ('AIRequest', AIRequest),
        ]
        
        for name, model in models:
            count = model.objects.count()
            print_success(f"{name} model: {count} records")
        
        return True
    except Exception as e:
        print_error(f"Model verification failed: {e}")
        return False

def verify_database():
    """Verify database connection and data"""
    print_header("Verifying Database")
    
    try:
        # Check if data exists
        user_count = User.objects.count()
        product_count = Product.objects.count()
        
        if user_count == 0:
            print_error("No users found. Run: python seed_data.py")
            return False
        
        if product_count < 200:
            print_error(f"Only {product_count} products found. Expected 200+")
            print_info("Run: python seed_data.py")
            return False
        
        print_success(f"Database populated: {user_count} users, {product_count} products")
        return True
    except Exception as e:
        print_error(f"Database verification failed: {e}")
        return False

def verify_admin_user():
    """Verify admin user exists"""
    print_header("Verifying Admin User")
    
    try:
        admin = User.objects.filter(username='admin').first()
        if admin:
            print_success("Admin user exists")
            print_info(f"Username: admin")
            print_info(f"Email: {admin.email}")
            print_info(f"Is superuser: {admin.is_superuser}")
            return True
        else:
            print_error("Admin user not found")
            print_info("Run: python seed_data.py")
            return False
    except Exception as e:
        print_error(f"Admin verification failed: {e}")
        return False

def verify_settings():
    """Verify Django settings"""
    print_header("Verifying Settings")
    
    try:
        from django.conf import settings
        
        print_success(f"DEBUG: {settings.DEBUG}")
        print_success(f"Database: {settings.DATABASES['default']['ENGINE']}")
        print_success(f"AI Mock Mode: {settings.AI_MOCK_MODE}")
        
        if settings.OPENAI_API_KEY:
            print_success("OpenAI API Key: Configured")
        else:
            print_info("OpenAI API Key: Not configured (using mock mode)")
        
        return True
    except Exception as e:
        print_error(f"Settings verification failed: {e}")
        return False

def verify_apps():
    """Verify all apps are installed"""
    print_header("Verifying Installed Apps")
    
    try:
        from django.conf import settings
        
        required_apps = [
            'users',
            'stores',
            'products',
            'orders',
            'ai_assistant',
            'news',
            'rest_framework',
            'rest_framework_simplejwt',
        ]
        
        installed = settings.INSTALLED_APPS
        
        for app in required_apps:
            if any(app in installed_app for installed_app in installed):
                print_success(f"{app}")
            else:
                print_error(f"{app} not found")
                return False
        
        return True
    except Exception as e:
        print_error(f"App verification failed: {e}")
        return False

def verify_urls():
    """Verify URL configuration"""
    print_header("Verifying URL Configuration")
    
    try:
        from django.urls import get_resolver
        
        resolver = get_resolver()
        url_patterns = [pattern.pattern._route for pattern in resolver.url_patterns if hasattr(pattern.pattern, '_route')]
        
        required_urls = [
            'admin/',
            'api/auth/',
            'api/stores/',
            'api/products/',
            'api/orders/',
            'api/ai/',
            'api/news/',
        ]
        
        for url in required_urls:
            if any(url in pattern for pattern in url_patterns):
                print_success(f"{url}")
            else:
                print_error(f"{url} not found")
                return False
        
        return True
    except Exception as e:
        print_error(f"URL verification failed: {e}")
        return False

def print_summary(results):
    """Print verification summary"""
    print_header("Verification Summary")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\nTotal Checks: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n" + "=" * 60)
        print("  ✓ ALL CHECKS PASSED!")
        print("  Your installation is ready to use!")
        print("=" * 60)
        print("\nNext Steps:")
        print("  1. Start server: python manage.py runserver")
        print("  2. Visit API docs: http://localhost:8000/api/docs/")
        print("  3. Visit admin: http://localhost:8000/admin/")
        print("  4. Login with: username='admin', password='admin123'")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("  ✗ SOME CHECKS FAILED")
        print("  Please fix the issues above")
        print("=" * 60)

def main():
    """Main verification function"""
    print("\n" + "=" * 60)
    print("  AI-Powered Ecommerce Marketplace")
    print("  Installation Verification")
    print("=" * 60)
    
    results = {
        'Settings': verify_settings(),
        'Apps': verify_apps(),
        'URLs': verify_urls(),
        'Models': verify_models(),
        'Database': verify_database(),
        'Admin User': verify_admin_user(),
    }
    
    print_summary(results)
    
    return all(results.values())

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
