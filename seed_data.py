"""
Seed script to generate sample data for the ecommerce marketplace
Generates 200+ products with categories, brands, stores, and users
"""
import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from stores.models import Store
from products.models import Product, Category, Brand, ProductImage
from news.models import NewsArticle
from faker import Faker

User = get_user_model()
fake = Faker()

# Sample data
CATEGORIES_DATA = [
    {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
    {'name': 'Clothing', 'description': 'Fashion and apparel'},
    {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
    {'name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear'},
    {'name': 'Books', 'description': 'Books and educational materials'},
    {'name': 'Toys & Games', 'description': 'Toys and gaming products'},
    {'name': 'Health & Beauty', 'description': 'Health and beauty products'},
    {'name': 'Automotive', 'description': 'Auto parts and accessories'},
    {'name': 'Food & Beverages', 'description': 'Food and drink products'},
    {'name': 'Office Supplies', 'description': 'Office and stationery items'},
]

BRANDS_DATA = [
    'TechPro', 'StyleMax', 'HomeEssentials', 'SportFit', 'ReadWell',
    'PlayTime', 'BeautyGlow', 'AutoParts Plus', 'FreshFood', 'OfficeHub',
    'EliteGear', 'UrbanStyle', 'ComfortHome', 'ActiveLife', 'SmartTech'
]

PRODUCT_ADJECTIVES = [
    'Premium', 'Professional', 'Deluxe', 'Essential', 'Advanced',
    'Classic', 'Modern', 'Vintage', 'Eco-Friendly', 'Luxury'
]

PRODUCT_TYPES = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera', 'Speaker', 'Monitor', 'Keyboard'],
    'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes', 'Hat', 'Sweater', 'Shorts'],
    'Home & Garden': ['Lamp', 'Cushion', 'Rug', 'Plant Pot', 'Tool Set', 'Furniture', 'Decor', 'Storage'],
    'Sports & Outdoors': ['Bicycle', 'Tent', 'Backpack', 'Yoga Mat', 'Dumbbells', 'Running Shoes', 'Ball', 'Racket'],
    'Books': ['Novel', 'Textbook', 'Magazine', 'Comic', 'Journal', 'Guide', 'Dictionary', 'Cookbook'],
    'Toys & Games': ['Board Game', 'Puzzle', 'Action Figure', 'Doll', 'Building Blocks', 'Card Game', 'RC Car', 'Plush Toy'],
    'Health & Beauty': ['Skincare Set', 'Makeup Kit', 'Perfume', 'Hair Dryer', 'Massage Tool', 'Vitamins', 'Soap', 'Lotion'],
    'Automotive': ['Car Cover', 'Floor Mats', 'Phone Mount', 'Dash Cam', 'Tool Kit', 'Air Freshener', 'Seat Covers', 'Wax'],
    'Food & Beverages': ['Coffee', 'Tea', 'Snacks', 'Spices', 'Sauce', 'Chocolate', 'Juice', 'Nuts'],
    'Office Supplies': ['Notebook', 'Pen Set', 'Desk Organizer', 'Calculator', 'Stapler', 'Paper', 'Folder', 'Tape'],
}


def create_users(count=10):
    """Create sample users"""
    print(f"Creating {count} users...")
    users = []
    
    # Create admin user
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@ecommerce.com',
            'user_type': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_verified': True,
            'first_name': 'Admin',
            'last_name': 'User'
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
    users.append(admin)
    
    # Create vendor users
    for i in range(count - 1):
        user, created = User.objects.get_or_create(
            username=f'vendor{i+1}',
            defaults={
                'email': f'vendor{i+1}@ecommerce.com',
                'user_type': 'vendor',
                'is_verified': True,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'phone': fake.phone_number()[:20],
                'city': fake.city(),
                'country': fake.country()
            }
        )
        if created:
            user.set_password('password123')
            user.save()
        users.append(user)
    
    print(f"Created {len(users)} users")
    return users



def create_categories():
    """Create product categories"""
    print("Creating categories...")
    categories = []
    for cat_data in CATEGORIES_DATA:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description'], 'is_active': True}
        )
        categories.append(category)
    print(f"Created {len(categories)} categories")
    return categories


def create_brands():
    """Create product brands"""
    print("Creating brands...")
    brands = []
    for brand_name in BRANDS_DATA:
        brand, created = Brand.objects.get_or_create(
            name=brand_name,
            defaults={
                'description': f'{brand_name} - Quality products you can trust',
                'is_active': True
            }
        )
        brands.append(brand)
    print(f"Created {len(brands)} brands")
    return brands


def create_stores(users):
    """Create stores for vendors"""
    print("Creating stores...")
    stores = []
    for user in users:
        if user.user_type == 'vendor':
            store_count = random.randint(1, 3)
            for i in range(store_count):
                store, created = Store.objects.get_or_create(
                    owner=user,
                    name=f"{user.first_name}'s {fake.company()} Store {i+1}",
                    defaults={
                        'description': fake.text(max_nb_chars=200),
                        'status': 'active',
                        'email': user.email,
                        'phone': user.phone,
                        'city': fake.city(),
                        'country': fake.country()
                    }
                )
                stores.append(store)
    print(f"Created {len(stores)} stores")
    return stores


def create_products(stores, categories, brands, count=250):
    """Create sample products"""
    print(f"Creating {count} products...")
    products = []
    
    for i in range(count):
        store = random.choice(stores)
        category = random.choice(categories)
        brand = random.choice(brands)
        
        product_types = PRODUCT_TYPES.get(category.name, ['Product'])
        product_type = random.choice(product_types)
        adjective = random.choice(PRODUCT_ADJECTIVES)
        
        name = f"{adjective} {product_type} #{i+1}"
        price = Decimal(random.uniform(9.99, 999.99)).quantize(Decimal('0.01'))
        compare_price = price * Decimal(random.uniform(1.2, 1.5))
        
        product = Product.objects.create(
            name=name,
            store=store,
            category=category,
            brand=brand,
            description=fake.text(max_nb_chars=500),
            short_description=fake.text(max_nb_chars=150),
            price=price,
            compare_price=compare_price.quantize(Decimal('0.01')),
            quantity=random.randint(0, 500),
            status=random.choice(['published', 'published', 'published', 'draft']),
            is_featured=random.choice([True, False, False, False]),
            tags=', '.join(fake.words(nb=5)),
            sku=f'SKU-{fake.unique.random_number(digits=8)}',
            meta_title=f"Buy {name} Online",
            meta_description=f"Shop {name} at great prices. {fake.text(max_nb_chars=100)}"
        )
        products.append(product)
        
        if i % 50 == 0:
            print(f"  Created {i} products...")
    
    print(f"Created {len(products)} products")
    return products


def create_news_articles(users, count=20):
    """Create sample news articles"""
    print(f"Creating {count} news articles...")
    articles = []
    
    for i in range(count):
        author = random.choice([u for u in users if u.user_type in ['admin', 'vendor']])
        
        article, created = NewsArticle.objects.get_or_create(
            title=fake.sentence(nb_words=8),
            author=author,
            defaults={
                'content': '\n\n'.join(fake.paragraphs(nb=5)),
                'excerpt': fake.text(max_nb_chars=200),
                'status': random.choice(['published', 'published', 'draft']),
                'tags': ', '.join(fake.words(nb=4)),
                'published_at': fake.date_time_this_year() if random.choice([True, False]) else None
            }
        )
        articles.append(article)
    
    print(f"Created {len(articles)} articles")
    return articles


def main():
    """Main seed function"""
    print("=" * 50)
    print("Starting database seeding...")
    print("=" * 50)
    
    users = create_users(10)
    categories = create_categories()
    brands = create_brands()
    stores = create_stores(users)
    products = create_products(stores, categories, brands, 250)
    articles = create_news_articles(users, 20)
    
    print("=" * 50)
    print("Database seeding completed!")
    print("=" * 50)
    print(f"Summary:")
    print(f"  Users: {len(users)}")
    print(f"  Categories: {len(categories)}")
    print(f"  Brands: {len(brands)}")
    print(f"  Stores: {len(stores)}")
    print(f"  Products: {len(products)}")
    print(f"  News Articles: {len(articles)}")
    print("=" * 50)
    print("\nDefault credentials:")
    print("  Admin: username='admin', password='admin123'")
    print("  Vendors: username='vendor1-9', password='password123'")
    print("=" * 50)


if __name__ == '__main__':
    main()
