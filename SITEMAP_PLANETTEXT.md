# AI-Powered Ecommerce Platform - Site Map for PlanetText

## Site Structure Overview

```
AI Ecommerce Platform
│
├── Public Pages (No Authentication Required)
│   ├── Home (Landing Page)
│   ├── Shop (Product Browsing)
│   ├── Login
│   └── Register
│
├── Seller Dashboard (Authentication Required)
│   ├── Dashboard Home
│   ├── AI Store Builder
│   ├── My Stores
│   ├── Products Management
│   ├── Categories
│   └── Orders
│
└── Admin Panel (Admin Only)
    ├── User Management
    ├── Store Approval
    └── System Settings
```

---

## Detailed Site Map for PlanetText

### 1. HOME PAGE (/)
**Purpose**: Landing page introducing the platform  
**Access**: Public  
**Key Elements**:
- Hero section with value proposition
- "AI-Powered Store Creation" badge
- Call-to-action buttons (Get Started, Watch Demo)
- Features showcase
- How it works (3-step process)
- Testimonials/social proof
- Footer with links

**Navigation Links**:
- → Shop (Browse Products)
- → Features (Anchor link)
- → How It Works (Anchor link)
- → Login
- → Register (Primary CTA)

**User Flow**:
```
Home → Register → Dashboard → AI Store Builder → Store Created
Home → Shop → Browse Products → AI Assistant
Home → Login → Dashboard
```

---

### 2. SHOP PAGE (/shop)
**Purpose**: Public product browsing with AI assistant  
**Access**: Public  
**Key Elements**:
- Product grid (all stores)
- Search bar (traditional)
- AI Assistant floating button (✨)
- Product cards with images, prices, categories
- Filter options
- "Show All Products" button

**AI Assistant Panel**:
- Chat interface
- Natural language search
- Quick example queries
- Real-time product recommendations

**Navigation Links**:
- → Home
- → Product Details (future)
- → Seller Login
- → AI Assistant (toggle)

**User Flow**:
```
Shop → Browse Products → Use AI Assistant → Get Recommendations
Shop → Search Products → View Results
Shop → Filter by Category/Price → View Filtered Products
```

---

### 3. LOGIN PAGE (/login)
**Purpose**: User authentication  
**Access**: Public  
**Key Elements**:
- Email/username input
- Password input
- "Remember me" checkbox
- Login button
- "Forgot password?" link
- "Don't have an account? Register" link

**Navigation Links**:
- → Register
- → Forgot Password (future)
- → Dashboard (after successful login)

**User Flow**:
```
Login → Enter Credentials → Dashboard
Login → Register (if no account)
```

---

### 4. REGISTER PAGE (/register)
**Purpose**: New user registration  
**Access**: Public  
**Key Elements**:
- Username input
- Email input
- Password input
- Confirm password input
- Terms acceptance checkbox
- Register button
- "Already have an account? Login" link

**Validation**:
- Username: min 3 characters
- Password: min 8 characters
- Password confirmation match

**Navigation Links**:
- → Login
- → Dashboard (after successful registration)

**User Flow**:
```
Register → Fill Form → Auto-login → Dashboard
Register → Login (if already have account)
```

---

### 5. DASHBOARD HOME (/dashboard)
**Purpose**: Main seller dashboard overview  
**Access**: Authenticated users only  
**Key Elements**:
- Welcome message
- Quick stats cards (stores, products, orders)
- Recent activity
- Quick action buttons
- Navigation sidebar

**Stats Displayed**:
- Total Stores
- Total Products
- Total Orders
- Revenue (future)

**Navigation Links**:
- → AI Store Builder
- → My Stores
- → Products
- → Categories
- → Orders
- → Profile Settings

**User Flow**:
```
Dashboard → View Stats → Navigate to Section
Dashboard → Quick Actions → Create Store/Product
```

---

### 6. AI STORE BUILDER (/ai)
**Purpose**: AI-powered store creation  
**Access**: Authenticated users only  
**Key Elements**:
- Chat interface with AI
- Input box for store idea
- Example prompts
- "Generate Store" button
- Loading state with progress
- Success message with store details
- Created store summary

**AI Interaction**:
1. User describes store idea
2. AI generates store structure
3. System creates store, categories, products
4. Display results with links

**Navigation Links**:
- → My Stores (view created store)
- → Products (view generated products)
- → Dashboard

**User Flow**:
```
AI Builder → Enter Idea → AI Generates → Store Created → View Store
AI Builder → Use Example → Generate → Success
```

**Example Inputs**:
- "I want a sports clothing store"
- "organic coffee shop"
- "handmade jewelry"
- "pet supplies"

---

### 7. MY STORES (/stores)
**Purpose**: List and manage user's stores  
**Access**: Authenticated users only  
**Key Elements**:
- Store cards grid
- Store information (name, description, status)
- Product count per store
- Creation date
- Action buttons (Manage, Delete)
- "Create Store with AI" button
- Empty state with CTA

**Store Card Info**:
- Store name
- Description
- Status badge (Active/Inactive)
- Products count
- Created date
- Manage button
- Delete button

**Navigation Links**:
- → AI Store Builder (create new)
- → Store Details (/stores/{slug})
- → Dashboard

**User Flow**:
```
My Stores → View List → Manage Store → Edit Details
My Stores → Create New → AI Builder
My Stores → Delete Store → Confirm
```

---

### 8. STORE DETAILS (/stores/{slug})
**Purpose**: View and edit individual store  
**Access**: Store owner only  
**Key Elements**:
- Store information form
- Name, tagline, description inputs
- Status selector
- Save/Cancel buttons
- Products sidebar (list of store products)
- Store statistics

**Editable Fields**:
- Store name
- Tagline
- Description
- Status (Active/Inactive/Pending)

**Products Sidebar**:
- List of products (first 5)
- Product name, price, status
- "View All Products" link

**Navigation Links**:
- → My Stores (back)
- → Products (view all)
- → Add Product

**User Flow**:
```
Store Details → Edit Information → Save → Updated
Store Details → View Products → Manage Products
Store Details → Back to My Stores
```

---

### 9. PRODUCTS PAGE (/products)
**Purpose**: List and manage all products  
**Access**: Authenticated users only  
**Key Elements**:
- Products grid
- Search bar
- Filter options
- Product cards with images
- Action buttons (Edit, Delete)
- "Add Product" button
- Empty state with CTA

**Product Card Info**:
- Product image
- Name
- Short description
- Price (with compare price)
- Category badge
- Status badge
- Stock quantity
- Edit/Delete buttons

**Navigation Links**:
- → Add Product (/products/new)
- → Edit Product (/products/{slug}/edit)
- → Dashboard

**User Flow**:
```
Products → View List → Search/Filter → View Results
Products → Add New → Create Product
Products → Edit → Update Product
Products → Delete → Confirm
```

---

### 10. CREATE PRODUCT (/products/new)
**Purpose**: Create new product  
**Access**: Authenticated users only  
**Key Elements**:
- Product information form
- Store selector
- Category selector
- AI Enhancement button
- Image upload (future)
- SEO section
- Save/Cancel buttons

**Form Sections**:

**Basic Information**:
- Store (dropdown)
- Category (dropdown)
- Product name
- Short description
- Full description
- Price
- Compare price
- Quantity
- SKU
- Tags
- Status

**SEO Information**:
- Meta title
- Meta description

**AI Enhancement**:
- "Enhance with AI" button
- Auto-fills: title, description, tags, meta fields

**Navigation Links**:
- → Products (back)
- → Dashboard

**User Flow**:
```
Create Product → Fill Form → Use AI Enhancement → Save → Products List
Create Product → Manual Entry → Save → Success
```

---

### 11. EDIT PRODUCT (/products/{slug}/edit)
**Purpose**: Edit existing product  
**Access**: Product owner only  
**Key Elements**:
- Pre-filled product form
- Same fields as create
- AI Enhancement button
- Save/Cancel buttons
- Delete button

**Navigation Links**:
- → Products (back)
- → Dashboard

**User Flow**:
```
Edit Product → Modify Fields → Save → Updated
Edit Product → Use AI → Enhance → Save
Edit Product → Delete → Confirm → Products List
```

---

### 12. CATEGORIES PAGE (/categories)
**Purpose**: View all product categories  
**Access**: Authenticated users only  
**Key Elements**:
- Categories grid
- Category cards
- Category name, description
- Product count per category
- Active/Inactive status
- Empty state

**Category Card Info**:
- Category name
- Description
- Product count
- Status badge

**Navigation Links**:
- → Dashboard
- → Products (filtered by category)

**User Flow**:
```
Categories → View List → Click Category → View Products
Categories → Browse → Dashboard
```

---

### 13. ORDERS PAGE (/orders)
**Purpose**: View and manage orders  
**Access**: Authenticated users only  
**Key Elements**:
- Orders list
- Order cards
- Order number, date
- Status badges
- Payment status
- Customer info
- Total amount
- Items count
- Empty state

**Order Card Info**:
- Order number
- Creation date
- Status (Processing/Shipped/Delivered/Cancelled)
- Payment status (Paid/Pending)
- Items count
- Total amount
- Shipping address

**Navigation Links**:
- → Dashboard
- → Order Details (future)

**User Flow**:
```
Orders → View List → Check Status
Orders → Filter by Status → View Results
```

---

## Navigation Structure

### Main Navigation (Sidebar - Authenticated Users)

```
Dashboard
├── Dashboard Home
├── AI Store Builder
├── My Stores
├── Products
│   ├── All Products
│   ├── Add Product
│   └── Categories
├── Orders
└── Profile (future)
```

### Top Navigation (Public)

```
Header
├── Logo (→ Home)
├── Shop
├── Features
├── How It Works
└── Login / Register
```

### Footer (Public)

```
Footer
├── About
├── Contact
├── Terms
├── Privacy
└── Social Links
```

---

## User Flows

### Flow 1: New Seller Registration to First Store

```
1. Home Page
2. Click "Get Started" → Register Page
3. Fill registration form → Submit
4. Auto-redirect to Dashboard
5. Click "AI Store Builder" → AI Page
6. Enter store idea → Generate
7. Store created → View in My Stores
8. Manage store → Add more products
```

### Flow 2: Customer Shopping Experience

```
1. Home Page
2. Click "Shop" → Shop Page
3. Browse products
4. Click AI Assistant (✨)
5. Ask "I need running shoes under $100"
6. AI shows recommendations
7. View filtered products
8. Click product (future: add to cart)
```

### Flow 3: Seller Product Management

```
1. Login → Dashboard
2. Click "Products" → Products Page
3. Click "Add Product" → Create Product Page
4. Fill basic info
5. Click "Enhance with AI"
6. AI fills SEO fields
7. Save product
8. Product appears in list
```

### Flow 4: AI Store Creation

```
1. Dashboard → AI Store Builder
2. Enter: "organic coffee shop"
3. AI generates:
   - Store name: "Organic Coffee Shop Store"
   - 4 categories
   - 8 sample products
4. Store created in database
5. Redirect to My Stores
6. View new store with products
```

---

## Page Relationships

```
┌─────────────────────────────────────────────────────────┐
│                      HOME PAGE                          │
│  (Landing, Features, How It Works)                      │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             ▼                            ▼
      ┌──────────┐                 ┌──────────┐
      │   SHOP   │                 │  LOGIN   │
      │ (Public) │                 │ (Public) │
      └──────────┘                 └─────┬────┘
             │                            │
             │                            ▼
             │                     ┌──────────┐
             │                     │ REGISTER │
             │                     │ (Public) │
             │                     └─────┬────┘
             │                            │
             │                            ▼
             │                   ┌─────────────────┐
             │                   │   DASHBOARD     │
             │                   │ (Authenticated) │
             │                   └────────┬────────┘
             │                            │
             │         ┌──────────────────┼──────────────────┐
             │         │                  │                  │
             │         ▼                  ▼                  ▼
             │   ┌──────────┐      ┌──────────┐      ┌──────────┐
             │   │ AI STORE │      │   MY     │      │ PRODUCTS │
             │   │ BUILDER  │      │  STORES  │      │   LIST   │
             │   └──────────┘      └─────┬────┘      └─────┬────┘
             │                            │                  │
             │                            ▼                  ▼
             │                     ┌──────────┐      ┌──────────┐
             │                     │  STORE   │      │  CREATE  │
             │                     │ DETAILS  │      │ PRODUCT  │
             │                     └──────────┘      └──────────┘
             │                                              │
             │                                              ▼
             │                                       ┌──────────┐
             │                                       │   EDIT   │
             │                                       │ PRODUCT  │
             │                                       └──────────┘
             │
             └──────────────────────────────────────────────────┘
```

---

## Access Control Matrix

| Page | Public | Authenticated | Owner Only | Admin Only |
|------|--------|---------------|------------|------------|
| Home | ✅ | ✅ | ✅ | ✅ |
| Shop | ✅ | ✅ | ✅ | ✅ |
| Login | ✅ | ✅ | ✅ | ✅ |
| Register | ✅ | ✅ | ✅ | ✅ |
| Dashboard | ❌ | ✅ | ✅ | ✅ |
| AI Store Builder | ❌ | ✅ | ✅ | ✅ |
| My Stores | ❌ | ✅ | ✅ | ✅ |
| Store Details | ❌ | ❌ | ✅ | ✅ |
| Products | ❌ | ✅ | ✅ | ✅ |
| Create Product | ❌ | ✅ | ✅ | ✅ |
| Edit Product | ❌ | ❌ | ✅ | ✅ |
| Categories | ❌ | ✅ | ✅ | ✅ |
| Orders | ❌ | ✅ | ✅ | ✅ |

---

## Mobile Navigation

### Hamburger Menu (Mobile)
```
☰ Menu
├── Home
├── Shop
├── Dashboard (if logged in)
├── My Stores (if logged in)
├── Products (if logged in)
├── Orders (if logged in)
├── Login (if not logged in)
└── Logout (if logged in)
```

---

## Search & Filter Options

### Shop Page Filters
- Search by keyword
- Filter by category
- Filter by price range (min/max)
- Filter by store
- Sort by: Price, Date, Featured

### Products Page Filters
- Search by name
- Filter by store
- Filter by category
- Filter by status
- Sort by: Date, Name, Price

---

## Call-to-Action Buttons

### Primary CTAs
1. **Home Page**: "Get Started Free" → Register
2. **Shop Page**: AI Assistant Button (✨)
3. **Dashboard**: "Create Store with AI" → AI Builder
4. **My Stores**: "Create Store with AI" → AI Builder
5. **Products**: "Add Product" → Create Product

### Secondary CTAs
1. **Home Page**: "Watch Demo"
2. **Login Page**: "Register"
3. **Register Page**: "Login"
4. **Dashboard**: Quick action cards

---

## Implementation Notes for PlanetText

### Page Hierarchy
```
Level 1: Home, Shop, Login, Register
Level 2: Dashboard, AI Builder, My Stores, Products, Categories, Orders
Level 3: Store Details, Create Product, Edit Product
```

### URL Structure
```
/                           → Home
/shop                       → Shop
/login                      → Login
/register                   → Register
/dashboard                  → Dashboard
/ai                         → AI Store Builder
/stores                     → My Stores
/stores/{slug}              → Store Details
/products                   → Products List
/products/new               → Create Product
/products/{slug}/edit       → Edit Product
/categories                 → Categories
/orders                     → Orders
```

### Meta Information

**Home Page**
- Title: "AI-Powered Ecommerce Platform | Create Your Store in Minutes"
- Description: "Transform your business idea into a fully functional online store using AI. No coding required."

**Shop Page**
- Title: "Shop All Products | AI Shopping Assistant"
- Description: "Browse products from all stores. Use our AI assistant to find exactly what you need."

**Dashboard**
- Title: "Dashboard | Manage Your Stores"
- Description: "Manage your online stores, products, and orders from one place."

---

This sitemap provides a complete structure for implementing the AI-Powered Ecommerce Platform on PlanetText or any website builder.
