# API Documentation

Complete API reference for the AI-Powered Ecommerce Marketplace.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Get Access Token

**Endpoint**: `POST /api/auth/login/`

**Request**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## API Endpoints

### Authentication & Users

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepass123",
  "password2": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "vendor"
}
```

#### Get Current User Profile
```http
GET /api/auth/profile/
Authorization: Bearer <token>
```

#### Update Profile
```http
PUT /api/auth/profile/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "bio": "Experienced vendor"
}
```

### Stores

#### List All Stores
```http
GET /api/stores/
```

Query Parameters:
- `status`: Filter by status (active, inactive, pending)
- `city`: Filter by city
- `search`: Search in name and description

#### Create Store
```http
POST /api/stores/create/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My Awesome Store",
  "description": "Best products in town",
  "email": "store@example.com",
  "phone": "+1234567890",
  "city": "New York",
  "country": "USA"
}
```

#### Get Store Details
```http
GET /api/stores/<slug>/
```

#### Update Store
```http
PUT /api/stores/<slug>/
Authorization: Bearer <token>
Content-Type: application/json

{
  "description": "Updated description",
  "status": "active"
}
```

#### Get My Stores
```http
GET /api/stores/my-stores/
Authorization: Bearer <token>
```

### Products

#### List Products
```http
GET /api/products/
```

Query Parameters:
- `store`: Filter by store ID
- `category`: Filter by category ID
- `brand`: Filter by brand ID
- `status`: Filter by status
- `is_featured`: Filter featured products
- `search`: Search in name, description, tags
- `ordering`: Sort by price, created_at, name

#### Create Product
```http
POST /api/products/create/
Authorization: Bearer <token>
Content-Type: application/json

{
  "store": 1,
  "category": 1,
  "brand": 1,
  "name": "Premium Wireless Headphones",
  "description": "High-quality wireless headphones with noise cancellation",
  "short_description": "Premium audio experience",
  "price": "199.99",
  "compare_price": "249.99",
  "quantity": 50,
  "status": "published",
  "tags": "wireless, audio, premium",
  "sku": "WH-001"
}
```

#### Get Product Details
```http
GET /api/products/<slug>/
```

#### Update Product
```http
PUT /api/products/<slug>/
Authorization: Bearer <token>
Content-Type: application/json

{
  "price": "179.99",
  "quantity": 45,
  "status": "published"
}
```

#### Delete Product
```http
DELETE /api/products/<slug>/
Authorization: Bearer <token>
```

### Categories

#### List Categories
```http
GET /api/products/categories/
```

#### Create Category
```http
POST /api/products/categories/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Smart Home Devices",
  "description": "IoT and smart home products",
  "parent": null
}
```

#### Get Category Details
```http
GET /api/products/categories/<slug>/
```

### Brands

#### List Brands
```http
GET /api/products/brands/
```

#### Create Brand
```http
POST /api/products/brands/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "TechPro",
  "description": "Premium technology brand",
  "website": "https://techpro.com"
}
```

### Orders

#### List My Orders
```http
GET /api/orders/
Authorization: Bearer <token>
```

#### Create Order
```http
POST /api/orders/create/
Authorization: Bearer <token>
Content-Type: application/json

{
  "total_amount": "299.99",
  "shipping_address": "123 Main St, New York, NY 10001",
  "billing_address": "123 Main St, New York, NY 10001",
  "phone": "+1234567890",
  "email": "customer@example.com",
  "notes": "Please deliver before 5 PM"
}
```

#### Get Order Details
```http
GET /api/orders/<id>/
Authorization: Bearer <token>
```

### AI Assistant

#### Product Assist
Enhance product information with AI.

```http
POST /api/ai/product-assist/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Wireless Headphones",
  "description": "Good quality headphones with bluetooth",
  "category": "Electronics",
  "price": "99.99"
}
```

**Response**:
```json
{
  "improved_title": "Premium Wireless Headphones - High Quality Bluetooth Audio",
  "seo_description": "Discover our Premium Wireless Headphones with advanced Bluetooth technology. Perfect for music lovers seeking exceptional sound quality and comfort. Features noise cancellation, long battery life, and premium build quality.",
  "category_suggestions": [
    "Electronics",
    "Audio & Headphones",
    "Wireless Accessories"
  ],
  "tags": [
    "wireless",
    "bluetooth",
    "audio",
    "premium",
    "headphones"
  ],
  "meta_title": "Buy Premium Wireless Headphones Online | Best Audio Quality",
  "meta_description": "Shop Premium Wireless Headphones at great prices. High-quality Bluetooth audio, noise cancellation, and comfort. Fast shipping available.",
  "tokens_used": 0
}
```

#### Store Generator
Generate complete store structure from an idea.

```http
POST /api/ai/store-generator/
Authorization: Bearer <token>
Content-Type: application/json

{
  "idea": "organic skincare products"
}
```

**Response**:
```json
{
  "store": {
    "name": "Organic Skincare Products Store",
    "description": "Your one-stop shop for all organic skincare products needs. Quality products at competitive prices.",
    "tagline": "Best organic skincare products marketplace"
  },
  "categories": [
    {
      "name": "Organic Skincare Products Essentials",
      "description": "Core products for daily skincare routine"
    },
    {
      "name": "Organic Skincare Products Premium",
      "description": "High-end luxury skincare selection"
    },
    {
      "name": "Organic Skincare Products Accessories",
      "description": "Complementary skincare tools and items"
    }
  ],
  "sample_products": [
    {
      "name": "Professional Organic Skincare Kit",
      "description": "Complete professional-grade organic skincare kit with all essentials including cleanser, toner, serum, and moisturizer",
      "price": 99.99,
      "category": "Organic Skincare Products Premium"
    },
    {
      "name": "Starter Organic Skincare Pack",
      "description": "Perfect starter pack for beginners in organic skincare with basic essentials",
      "price": 49.99,
      "category": "Organic Skincare Products Essentials"
    }
  ],
  "tokens_used": 0
}
```

#### AI Usage Statistics
```http
GET /api/ai/usage-stats/
Authorization: Bearer <token>
```

**Response**:
```json
{
  "total_requests": 15,
  "product_assist_count": 10,
  "store_generator_count": 5,
  "total_tokens_used": 0,
  "avg_processing_time": 0.25
}
```

### News/Blog

#### List Articles
```http
GET /api/news/
```

Query Parameters:
- `search`: Search in title and content

#### Create Article
```http
POST /api/news/create/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "10 Tips for Successful Online Selling",
  "content": "Full article content here...",
  "excerpt": "Learn the best practices for online selling",
  "status": "published",
  "tags": "ecommerce, tips, selling"
}
```

#### Get Article Details
```http
GET /api/news/<slug>/
```

## Response Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Pagination

List endpoints support pagination:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

Query Parameters:
- `page`: Page number
- `page_size`: Items per page (default: 20)

## Filtering & Search

Most list endpoints support:
- **Filtering**: `?category=1&status=published`
- **Search**: `?search=wireless`
- **Ordering**: `?ordering=-created_at` (prefix with `-` for descending)

## Error Responses

```json
{
  "detail": "Error message here"
}
```

Or for validation errors:
```json
{
  "field_name": ["Error message for this field"]
}
```

## Rate Limiting

Consider implementing rate limits:
- AI endpoints: 10 requests/minute
- Authentication: 5 requests/minute
- Other endpoints: 100 requests/minute

## Webhooks (Future)

Planned webhook events:
- `order.created`
- `order.updated`
- `product.created`
- `product.updated`

## SDK Examples

### Python
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'username': 'admin',
    'password': 'admin123'
})
token = response.json()['access']

# Create product with AI assistance
headers = {'Authorization': f'Bearer {token}'}
ai_response = requests.post(
    'http://localhost:8000/api/ai/product-assist/',
    headers=headers,
    json={
        'name': 'Smart Watch',
        'description': 'Fitness tracking watch'
    }
)
enhanced_data = ai_response.json()

# Create product
product_response = requests.post(
    'http://localhost:8000/api/products/create/',
    headers=headers,
    json={
        'store': 1,
        'name': enhanced_data['improved_title'],
        'description': enhanced_data['seo_description'],
        'price': '199.99',
        'quantity': 50
    }
)
```

### JavaScript
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});
const { access } = await loginResponse.json();

// Get products
const productsResponse = await fetch('http://localhost:8000/api/products/', {
  headers: { 'Authorization': `Bearer ${access}` }
});
const products = await productsResponse.json();
```

## Interactive Documentation

Visit the Swagger UI for interactive API testing:
```
http://localhost:8000/api/docs/
```

---

For more details, refer to the main README.md file.
