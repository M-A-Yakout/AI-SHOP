# AI-Powered Ecommerce Platform

> Transform your business idea into a fully functional online store in minutes using AI automation

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.1.0-black.svg)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

An innovative AI-powered ecommerce platform that automates the entire process of creating and managing online stores. Simply describe your business idea, and our AI will generate a complete store with products, categories, and everything you need to start selling.

### Key Highlights

- 🤖 **AI Store Generation**: Transform ideas into working stores in seconds
- 🛍️ **Smart Product Search**: AI-powered shopping assistant for customers
- 🏪 **Multi-Vendor Support**: Multiple stores on one platform
- 📦 **Complete CRUD**: Full product, category, and order management
- 🔐 **Secure Authentication**: JWT-based auth with role management
- 🎨 **Modern UI**: Beautiful, responsive Next.js frontend
- 🔍 **Advanced Search**: Django ORM-based search with filters
- 📊 **Real-time Updates**: Dynamic content with state management

## 🌟 Features

### For Store Owners

#### 1. **AI Store Builder**
- Describe your business idea in natural language
- AI generates store name, description, and tagline
- Automatically creates relevant product categories
- Generates sample products with descriptions and pricing
- Creates brand identity
- Store ready to use in under 60 seconds

#### 2. **Product Management**
- Create, read, update, delete products
- AI-powered product enhancement
- Automatic SEO optimization
- Image management
- Inventory tracking
- SKU and barcode support
- Price comparison and discounts
- Product variants and options

#### 3. **Store Management**
- Multiple stores per user
- Store customization
- Status management (active/inactive)
- Store analytics
- Product count tracking
- Store-specific branding

#### 4. **Category & Brand Management**
- Organize products by categories
- Brand management
- Category hierarchies
- Automatic slug generation
- SEO-friendly URLs

#### 5. **Order Management**
- View all orders
- Order status tracking
- Customer information
- Payment status
- Shipping details

### For Customers

#### 1. **Smart Shopping Experience**
- Browse all products from all stores
- Advanced search with filters
- AI Shopping Assistant
- Natural language product search
- Price filtering
- Category browsing
- Product recommendations

#### 2. **AI Shopping Assistant**
- Chat-based interface
- Natural language queries
- Intelligent product recommendations
- Price-aware suggestions
- Category-based filtering
- Real-time search results

## 🏗️ Architecture

### Backend (Django REST Framework)

```
project/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── users/                 # User management
│   ├── models.py          # Custom user model
│   ├── views.py           # Auth views
│   └── serializers.py     # User serializers
├── stores/                # Store management
│   ├── models.py          # Store model
│   ├── views.py           # Store CRUD
│   └── permissions.py     # Store permissions
├── products/              # Product management
│   ├── models.py          # Product, Category, Brand models
│   ├── views.py           # Product CRUD + Search
│   └── serializers.py     # Product serializers
├── orders/                # Order management
│   ├── models.py          # Order, OrderItem models
│   ├── views.py           # Order processing
│   └── serializers.py     # Order serializers
├── ai_assistant/          # AI integration
│   ├── services.py        # OpenAI integration
│   ├── automation.py      # Store automation
│   ├── views.py           # AI endpoints
│   └── models.py          # AI request logging
└── news/                  # News/blog system
    ├── models.py          # News articles
    └── views.py           # News CRUD
```

### Frontend (Next.js 14)

```
frontend/
├── app/
│   ├── (auth)/           # Authentication pages
│   │   ├── login/        # Login page
│   │   └── register/     # Registration page
│   ├── (dashboard)/      # Protected dashboard
│   │   ├── dashboard/    # Main dashboard
│   │   ├── products/     # Product management
│   │   ├── stores/       # Store management
│   │   ├── categories/   # Category listing
│   │   ├── orders/       # Order management
│   │   └── ai/           # AI store builder
│   ├── shop/             # Public shopping page
│   └── page.tsx          # Landing page
├── components/
│   ├── ui/               # Reusable UI components
│   └── layout/           # Layout components
├── services/             # API service layer
│   ├── auth.service.ts   # Authentication
│   ├── product.service.ts # Products
│   ├── store.service.ts  # Stores
│   ├── order.service.ts  # Orders
│   └── ai.service.ts     # AI features
├── store/                # State management (Zustand)
│   ├── useAuthStore.ts   # Auth state
│   ├── useProductStore.ts # Product state
│   └── useStoreStore.ts  # Store state
└── lib/
    ├── api.ts            # Axios configuration
    └── utils.ts          # Utility functions
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- npm or yarn
- SQLite (default) or PostgreSQL

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd project
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.example .env.local
# Edit .env.local with your settings
```

4. **Start development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_ENGINE=sqlite  # or postgresql

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo
AI_MOCK_MODE=False

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST_USER=noreply@example.com
EMAIL_HOST_PASSWORD=password123
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📡 API Endpoints

### Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/token/refresh/` - Refresh JWT token
- `GET /api/users/profile/` - Get user profile

### Stores
- `GET /api/stores/` - List all stores
- `GET /api/stores/my-stores/` - Get user's stores
- `POST /api/stores/create/` - Create new store
- `GET /api/stores/{slug}/` - Get store details
- `PUT /api/stores/{slug}/` - Update store
- `DELETE /api/stores/{slug}/` - Delete store

### Products
- `GET /api/products/` - List all products
- `GET /api/products/search/?q=query` - Search products
- `POST /api/products/create/` - Create product
- `GET /api/products/{slug}/` - Get product details
- `PUT /api/products/{slug}/` - Update product
- `DELETE /api/products/{slug}/` - Delete product

### Categories & Brands
- `GET /api/products/categories/` - List categories
- `GET /api/products/brands/` - List brands

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/create/` - Create order
- `GET /api/orders/{id}/` - Get order details

### AI Features
- `POST /api/ai/product-assist/` - AI product enhancement
- `POST /api/ai/store-generator/` - AI store structure generation
- `POST /api/ai/create-automated-store/` - Full store automation
- `POST /api/ai/search/` - AI-powered product search (public)
- `GET /api/ai/usage-stats/` - AI usage statistics

## 🤖 AI Integration

### OpenAI Features

1. **Product Enhancement**
   - Generates SEO-friendly titles
   - Creates compelling descriptions
   - Suggests relevant categories
   - Generates product tags
   - Creates meta titles and descriptions

2. **Store Generation**
   - Creates store name and description
   - Generates tagline
   - Suggests product categories
   - Creates sample products with pricing

3. **Shopping Assistant**
   - Natural language product search
   - Intelligent recommendations
   - Price-aware suggestions
   - Category-based filtering

### Mock Mode

The system includes a mock mode that works without OpenAI API:
- Set `AI_MOCK_MODE=True` in `.env`
- Provides template-based responses
- Useful for development and testing
- No API costs

## 🔍 Search Implementation

### Django ORM Search

All product searches use Django ORM with:
- Case-insensitive matching (`__icontains`)
- Multi-field search (name, description, tags, category)
- Keyword splitting for better results
- Price range filtering
- Category filtering
- Performance optimization with indexes
- Result pagination

### Search Features

```python
# Simple search
GET /api/products/search/?q=running+shoes

# Advanced search with filters
GET /api/products/search/?q=shoes&min_price=50&max_price=150&category=sports&limit=20
```

## 🎨 Frontend Features

### Technology Stack
- **Next.js 14** - App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Zustand** - State management
- **Axios** - HTTP client
- **React Hook Form** - Form handling

### Key Features
- Server-side rendering (SSR)
- Client-side navigation
- Responsive design
- Dark mode support
- Loading states
- Error handling
- Toast notifications
- Form validation

## 🔐 Security

- JWT authentication
- Password hashing (Django's PBKDF2)
- CORS configuration
- CSRF protection
- SQL injection prevention (ORM)
- XSS protection
- Secure password requirements
- Permission-based access control

## 📊 Database Schema

### Core Models

**User**
- Custom user model with email authentication
- Role-based permissions
- Profile information

**Store**
- Multi-vendor support
- Owner relationship
- Status management
- Contact information

**Product**
- Store relationship
- Category and brand relationships
- Pricing and inventory
- SEO fields
- Status management

**Category**
- Hierarchical structure
- SEO-friendly slugs
- Active/inactive status

**Order**
- User relationship
- Order items
- Payment status
- Shipping information

**AIRequest**
- Request logging
- Token usage tracking
- Performance metrics

## 🧪 Testing

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Deployment

### Backend Deployment

1. **Set production environment**
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

2. **Collect static files**
```bash
python manage.py collectstatic
```

3. **Use production database** (PostgreSQL recommended)

4. **Use production server** (Gunicorn, uWSGI)

### Frontend Deployment

1. **Build for production**
```bash
npm run build
```

2. **Deploy to Vercel/Netlify** or use:
```bash
npm start
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- OpenAI for GPT integration
- Django REST Framework team
- Next.js team
- shadcn/ui for beautiful components
- All contributors

## 📞 Support

For support, email support@example.com or open an issue in the repository.

## 🗺️ Roadmap

- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Shopping cart
- [ ] Checkout process
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Advanced AI features
- [ ] Social media integration
- [ ] SEO optimization tools
- [ ] Marketing automation

## 📚 Documentation

- [API Documentation](API_DOCUMENTATION.md)
- [Architecture Guide](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)
- [AI Integration Guide](AI_INTEGRATION_GUIDE.md)
- [Database Search Implementation](DATABASE_SEARCH_IMPLEMENTATION.md)

## 🔗 Links

- [Live Demo](#)
- [Documentation](#)
- [API Reference](#)
- [Issue Tracker](#)

---

Made with ❤️ using Django, Next.js, and AI
