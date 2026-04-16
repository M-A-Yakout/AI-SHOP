"""
Test script for the complete automation flow
Tests: Idea → Working Store
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from ai_assistant.automation import create_automated_store, StoreAutomationError

User = get_user_model()


def test_automation():
    """Test the complete automation flow"""
    print("=" * 80)
    print("TESTING FULL AUTOMATION: Idea → Working Store")
    print("=" * 80)
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='automation_test_user',
        defaults={
            'email': 'automation@test.com',
            'first_name': 'Automation',
            'last_name': 'Tester'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✓ Created test user: {user.username}")
    else:
        print(f"✓ Using existing user: {user.username}")
    
    print()
    
    # Test ideas
    test_ideas = [
        "sports clothing store",
        "organic coffee shop",
        "vintage books"
    ]
    
    for idx, idea in enumerate(test_ideas, 1):
        print(f"\n{'=' * 80}")
        print(f"TEST {idx}/{len(test_ideas)}: Creating store from idea: '{idea}'")
        print('=' * 80)
        
        try:
            # Run automation
            result = create_automated_store(user, idea)
            
            # Display results
            print(f"\n✅ SUCCESS! Store created: {result['store']['name']}")
            print(f"\n📊 SUMMARY:")
            print(f"   Store ID: {result['store']['id']}")
            print(f"   Store URL: {result['store']['url']}")
            print(f"   Status: {result['store']['status']}")
            print(f"   Categories: {result['summary']['total_categories']}")
            print(f"   Products: {result['summary']['total_products']}")
            print(f"   AI Mode: {result['summary']['ai_mode']}")
            print(f"   Processing Time: {result['summary']['processing_time']}s")
            
            print(f"\n📦 CATEGORIES CREATED:")
            for cat in result['categories']:
                print(f"   - {cat['name']} (slug: {cat['slug']})")
            
            print(f"\n🏷️  BRAND CREATED:")
            print(f"   - {result['brand']['name']} (slug: {result['brand']['slug']})")
            
            print(f"\n🛍️  PRODUCTS CREATED:")
            for prod in result['products'][:5]:  # Show first 5
                print(f"   - {prod['name']} (${prod['price']}) - {prod['category']}")
            
            if len(result['products']) > 5:
                print(f"   ... and {len(result['products']) - 5} more products")
            
            print(f"\n📝 NEXT STEPS:")
            for step in result['next_steps']:
                print(f"   • {step}")
            
        except StoreAutomationError as e:
            print(f"\n❌ AUTOMATION ERROR: {e}")
            return False
        except Exception as e:
            print(f"\n❌ UNEXPECTED ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print(f"\n{'=' * 80}")
    print("✅ ALL AUTOMATION TESTS PASSED!")
    print('=' * 80)
    
    return True


if __name__ == '__main__':
    try:
        success = test_automation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
