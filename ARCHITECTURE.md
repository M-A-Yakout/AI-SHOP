# System Architecture

## Overview

This is a production-ready, scalable multi-vendor ecommerce marketplace with AI-powered features built using Django and Django REST Framework.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  (React/Vue/Mobile App or API Consumers)                    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway / Load Balancer              │
│                     (Nginx / AWS ALB)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Django Application Layer                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Django REST Framework                                │  │
│  │  - JWT Authentication                                 │  │
│  │  - API Endpoints                                      │  │
│  │  - Serializers & Validators                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic Layer (Apps)                         │  │
│  │  ┌────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐    │  │
│  │  │ Users  │ │ Stores │ │Products │ │  Orders  │    │  │
│  │  └────────┘ └────────┘ └─────────┘ └──────────┘    │  │
│  │  ┌────────┐ ┌──────────────────┐                    │  │
│  │  │  News  │ │  AI Assistant    │                    │  │
│  │  └────────┘ └──────────────────┘                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│  PostgreSQL  │ │  Redis   │ │   OpenAI     │
│   Database   │ │  Cache   │ │     API      │
└──────────────┘ └──────────┘ └──────────────┘
        │
        ▼
┌──────────────┐
│  S3/Storage  │
│ (Media Files)│
└──────────────┘
```

## Application Structure

### Core Apps

#### 1. Users App
**Purpose**: Authentication and user management

**Models**:
- `User`: Custom user model with role-based access (Customer, Vendor, Admin)

**Key Features**:
- JWT authentication
- User registration and profile management
- Role-based permissions
- User verification system

**API Endpoints**:
- `/api/auth/register/` - User registration
- `/api/auth/login/` - JWT token generation
- `/api/auth/profile/` - Profile management

#### 2. Stores App
**Purpose**: Multi-vendor store management

**Models**:
- `Store`: Store information and settings

**Key Features**:
- Multiple stores per user
- Store status management (active, inactive, pending)
- Store-level permissions
- Slug-based URLs

**API Endpoints**:
- `/api/stores/` - List stores
- `/api/stores/create/` - Create store
- `/api/stores/my-stores/` - User's stores

#### 3. Products App
**Purpose**: Product catalog management

**Models**:
- `Product`: Main product information
- `Category`: Hierarchical product categories
- `Brand`: Product brands
- `ProductImage`: Product images with ordering

**Key Features**:
- Full CRUD operations
- Category hierarchy
- Product variants support (extensible)
- Image management
- SEO fields (meta title, description)
- Inventory tracking

**API Endpoints**:
- `/api/products/` - Product listing with filters
- `/api/products/create/` - Create product
- `/api/products/categories/` - Category management
- `/api/products/brands/` - Brand management

#### 4. Orders App
**Purpose**: Order processing and management

**Models**:
- `Order`: Order header information
- `OrderItem`: Order line items

**Key Features**:
- Order creation and tracking
- Order status workflow
- Payment status tracking
- Order history

**API Endpoints**:
- `/api/orders/` - List user orders
- `/api/orders/create/` - Create order
- `/api/orders/<id>/` - Order details

#### 5. AI Assistant App
**Purpose**: AI-powered product and store generation

**Models**:
- `AIRequest`: Track AI API usage and analytics

**Services**:
- `AIService`: OpenAI integration with mock fallback

**Key Features**:
- Product enhancement (titles, descriptions, tags)
- Store generation from ideas
- Category suggestions
- SEO optimization
- Usage tracking and analytics

**API Endpoints**:
- `/api/ai/product-assist/` - Enhance product data
- `/api/ai/store-generator/` - Generate store structure
- `/api/ai/usage-stats/` - AI usage statistics

#### 6. News App
**Purpose**: Content management for blog/news

**Models**:
- `NewsArticle`: Blog posts and news articles

**Key Features**:
- Article publishing workflow
- View count tracking
- Tag-based organization
- Featured images

**API Endpoints**:
- `/api/news/` - List articles
- `/api/news/create/` - Create article
- `/api/news/<slug>/` - Article details

## Data Flow

### Product Creation with AI

```
1. User submits product draft
   ↓
2. POST /api/ai/product-assist/
   ↓
3. AIService processes request
   ↓
4. OpenAI API (or mock) generates enhancements
   ↓
5. Enhanced data returned to user
   ↓
6. User creates product with enhanced data
   ↓
7. POST /api/products/create/
   ↓
8. Product saved to database
```

### Store Generation Flow

```
1. User provides store idea
   ↓
2. POST /api/ai/store-generator/
   ↓
3. AIService generates store structure
   ↓
4. Returns: store details, categories, sample products
   ↓
5. User can create store and products from generated data
```

## Database Schema

### Key Relationships

```
User (1) ──────── (N) Store
Store (1) ──────── (N) Product
Category (1) ──────── (N) Product
Brand (1) ──────── (N) Product
Product (1) ──────── (N) ProductImage
User (1) ──────── (N) Order
Order (1) ──────── (N) OrderItem
Product (1) ──────── (N) OrderItem
User (1) ──────── (N) NewsArticle
User (1) ──────── (N) AIRequest
```

### Indexes

Optimized indexes on:
- User email, user_type
- Store slug, owner, status
- Product slug, store, category, status
- Order order_number, customer, status
- Category slug
- Brand slug

## Security Architecture

### Authentication
- JWT-based authentication
- Access token (1 hour expiry)
- Refresh token (7 days expiry)
- Token rotation on refresh

### Authorization
- Role-based access control (RBAC)
- Custom permissions per app
- Object-level permissions
- Store owner verification

### Data Protection
- Password hashing (Django's PBKDF2)
- CSRF protection
- CORS configuration
- SQL injection prevention (ORM)
- XSS protection

## API Design Principles

### RESTful Design
- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Proper status codes
- Consistent response format

### Pagination
- Page-based pagination
- Configurable page size
- Default: 20 items per page

### Filtering & Search
- Query parameter filtering
- Full-text search
- Ordering support

### Versioning
- URL-based versioning (future)
- Backward compatibility

## Performance Optimization

### Database
- Indexed fields for fast queries
- Select related / prefetch related
- Database connection pooling
- Query optimization

### Caching Strategy
- Redis for session storage
- Cache frequently accessed data
- Cache invalidation on updates

### Static Files
- WhiteNoise for static file serving
- CDN for production
- Compressed assets

### Media Files
- Separate media storage
- Image optimization
- Lazy loading

## Scalability Considerations

### Horizontal Scaling
- Stateless application design
- Load balancer ready
- Session storage in Redis
- Shared media storage (S3)

### Vertical Scaling
- Database optimization
- Connection pooling
- Efficient queries

### Async Processing
- Celery for background tasks
- Email sending
- Report generation
- AI processing (optional)

## Monitoring & Logging

### Application Monitoring
- Error tracking (Sentry)
- Performance monitoring
- API response times
- Database query performance

### Logging
- Structured logging
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Log aggregation
- Audit trails

### Metrics
- Request count
- Response times
- Error rates
- AI API usage
- Database connections

## Deployment Architecture

### Development
```
SQLite → Django Dev Server → Local
```

### Production
```
PostgreSQL → Gunicorn → Nginx → Load Balancer → Internet
     ↓
   Redis
     ↓
  Celery Workers
```

## Technology Stack

### Backend
- **Framework**: Django 4.2+
- **API**: Django REST Framework 3.14+
- **Authentication**: djangorestframework-simplejwt
- **Database**: PostgreSQL / SQLite
- **Cache**: Redis
- **Task Queue**: Celery
- **AI**: OpenAI API

### Infrastructure
- **Web Server**: Gunicorn
- **Reverse Proxy**: Nginx
- **Static Files**: WhiteNoise
- **Media Storage**: Local / S3
- **Monitoring**: Sentry

### Development
- **Language**: Python 3.9+
- **Package Manager**: pip
- **Environment**: python-decouple
- **Testing**: Django Test Framework
- **Documentation**: drf-spectacular

## API Documentation

### Auto-generated Docs
- Swagger UI at `/api/docs/`
- OpenAPI 3.0 schema at `/api/schema/`
- Interactive testing interface

## Future Enhancements

### Phase 2
- Payment gateway integration (Stripe, PayPal)
- Product reviews and ratings
- Wishlist functionality
- Advanced search (Elasticsearch)
- Real-time notifications (WebSockets)

### Phase 3
- Multi-language support
- Multi-currency support
- Advanced analytics dashboard
- Inventory management
- Shipping integration

### Phase 4
- Mobile app API optimization
- GraphQL API
- Microservices architecture
- Event-driven architecture
- Machine learning recommendations

## Best Practices Implemented

1. **Clean Code**: Modular app structure
2. **DRY Principle**: Reusable serializers and views
3. **Security First**: JWT, permissions, validation
4. **Scalability**: Stateless design, caching ready
5. **Documentation**: Comprehensive API docs
6. **Testing Ready**: Test-friendly architecture
7. **Production Ready**: Environment-based config
8. **Maintainability**: Clear separation of concerns

---

This architecture supports 200-300+ products easily and can scale to thousands with proper infrastructure.
