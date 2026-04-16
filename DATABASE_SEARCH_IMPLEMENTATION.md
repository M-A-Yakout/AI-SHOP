# Database Search Implementation

## Overview
All product search and retrieval is now done directly from the database using Django ORM, with no external API calls.

## Changes Made

### 1. **Product Model** (`products/models.py`)
- ✅ Added `search()` class method for ORM-based product search
- ✅ Added database index on `name` field for better search performance
- ✅ Supports case-insensitive matching using `__icontains`
- ✅ Searches across: name, description, short_description, tags, category name, brand name
- ✅ Supports filters: min_price, max_price, category, store

**Usage Example:**
```python
# Simple search
products = Product.search("running shoes")

# Search with filters
products = Product.search("shoes", filters={
    'min_price': 50,
    'max_price': 150,
    'category': 'sports'
})
```

### 2. **Product Views** (`products/views.py`)
- ✅ Added `search_products()` view for direct database search
- ✅ Uses Django ORM with Q objects for complex queries
- ✅ Supports multiple query parameters:
  - `q`: Search query
  - `min_price`: Minimum price filter
  - `max_price`: Maximum price filter
  - `category`: Category slug
  - `limit`: Results limit (default: 20, max: 100)
- ✅ Returns paginated JSON response
- ✅ No authentication required (public endpoint)

**API Endpoint:**
```
GET /api/products/search/?q=running+shoes&min_price=50&max_price=150&limit=20
```

**Response Format:**
```json
{
  "success": true,
  "query": "running shoes",
  "total_count": 15,
  "returned_count": 15,
  "products": [...],
  "filters": {
    "min_price": "50",
    "max_price": "150",
    "category": null,
    "limit": 20
  }
}
```

### 3. **AI Search Assistant** (`ai_assistant/views.py`)
- ✅ Modified `product_search_assistant()` to use Django ORM
- ✅ Removed all external API calls for product retrieval
- ✅ Searches database using Q objects with OR conditions
- ✅ Splits query into keywords for better matching
- ✅ Uses `select_related()` for optimized database queries
- ✅ Limits results to 20 products
- ✅ AI provides helpful responses based on database results

**API Endpoint:**
```
POST /api/ai/search/
Body: {"query": "I need running shoes under $100"}
```

### 4. **URL Configuration** (`products/urls.py`)
- ✅ Added `/api/products/search/` endpoint
- ✅ Properly ordered URLs to avoid slug conflicts

## Search Features

### Case-Insensitive Matching
All searches use `__icontains` for case-insensitive matching:
```python
Q(name__icontains=keyword)
Q(description__icontains=keyword)
```

### Multi-Field Search
Searches across multiple fields simultaneously:
- Product name
- Description
- Short description
- Tags
- Category name
- Brand name

### Keyword Splitting
Query is split into keywords for better results:
```python
query = "running shoes"
keywords = ["running", "shoes"]
# Matches products containing either "running" OR "shoes"
```

### Performance Optimization
- ✅ Database indexes on frequently searched fields
- ✅ `select_related()` to reduce database queries
- ✅ `distinct()` to avoid duplicate results
- ✅ Result limiting to prevent large responses

### Filtering
Supports additional filters:
- Price range (min_price, max_price)
- Category filtering
- Store filtering
- Featured products prioritization

## Database Queries

### Example 1: Simple Search
```python
products = Product.objects.filter(
    Q(name__icontains='shoes') | 
    Q(description__icontains='shoes'),
    status='published'
).select_related('category', 'brand', 'store')
```

### Example 2: Multi-Keyword Search
```python
keywords = ['running', 'shoes']
q_objects = Q()
for keyword in keywords:
    q_objects |= Q(name__icontains=keyword)
    q_objects |= Q(description__icontains=keyword)

products = Product.objects.filter(
    q_objects, 
    status='published'
).distinct()
```

### Example 3: Search with Filters
```python
products = Product.objects.filter(
    Q(name__icontains='shoes'),
    status='published',
    price__gte=50,
    price__lte=150,
    category__slug='sports'
).select_related('category', 'brand', 'store')
```

## API Endpoints Summary

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/products/` | GET | No | List all published products |
| `/api/products/search/` | GET | No | Search products with filters |
| `/api/ai/search/` | POST | No | AI-powered search with recommendations |
| `/api/products/<slug>/` | GET | No | Get single product details |

## Testing

### Test Search Endpoint
```bash
# Simple search
curl "http://localhost:8000/api/products/search/?q=shoes"

# Search with filters
curl "http://localhost:8000/api/products/search/?q=shoes&min_price=50&max_price=150&category=sports&limit=10"
```

### Test AI Search
```bash
curl -X POST http://localhost:8000/api/ai/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "I need running shoes under $100"}'
```

## Benefits

1. **Performance**: Direct database queries are faster than external API calls
2. **Reliability**: No dependency on external services
3. **Scalability**: Can handle high query volumes
4. **Flexibility**: Easy to add new search criteria
5. **Cost**: No API usage costs
6. **Privacy**: All data stays in local database

## Future Enhancements

- [ ] Full-text search using PostgreSQL
- [ ] Search result ranking/scoring
- [ ] Search analytics and logging
- [ ] Autocomplete suggestions
- [ ] Fuzzy matching for typos
- [ ] Search history for users
- [ ] Popular searches tracking
