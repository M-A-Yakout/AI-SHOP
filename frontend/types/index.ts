export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: 'customer' | 'vendor' | 'admin';
  is_verified: boolean;
  avatar?: string;
}

export interface Store {
  id: number;
  name: string;
  slug: string;
  description: string;
  tagline?: string;
  logo?: string;
  banner?: string;
  status: 'active' | 'inactive' | 'pending';
  owner: number;
  created_at: string;
  updated_at: string;
  products_count?: number;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  image?: string;
  parent?: number;
  is_active: boolean;
  products_count?: number;
}

export interface Brand {
  id: number;
  name: string;
  slug: string;
  description?: string;
  logo?: string;
  website?: string;
  is_active: boolean;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  short_description?: string;
  price: string;
  compare_price?: string;
  cost_price?: string;
  sku?: string;
  barcode?: string;
  quantity: number;
  weight?: string;
  status: 'draft' | 'published' | 'out_of_stock';
  is_featured: boolean;
  store: number;
  category?: number;
  brand?: number;
  tags?: string;
  meta_title?: string;
  meta_description?: string;
  images?: ProductImage[];
  created_at: string;
  updated_at: string;
}

export interface ProductImage {
  id: number;
  image: string;
  alt_text?: string;
  is_primary: boolean;
  order: number;
}

export interface Order {
  id: number;
  order_number: string;
  user: number;
  store: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  payment_status: 'pending' | 'paid' | 'failed' | 'refunded';
  total_amount: string;
  shipping_address: string;
  billing_address?: string;
  notes?: string;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  id: number;
  product: number;
  product_name: string;
  quantity: number;
  price: string;
  total: string;
}

export interface AIRequest {
  id: number;
  user: number;
  request_type: 'product_assist' | 'store_generator' | 'full_automation';
  input_data: any;
  output_data: any;
  tokens_used?: number;
  processing_time?: number;
  created_at: string;
}

export interface ProductAssistRequest {
  name: string;
  description?: string;
  category?: string;
  price?: string;
}

export interface ProductAssistResponse {
  improved_title: string;
  seo_description: string;
  category_suggestions: string[];
  tags: string[];
  meta_title: string;
  meta_description: string;
  tokens_used?: number;
  mode: 'groq' | 'mock';
  processing_time?: number;
  success: boolean;
}

export interface StoreGeneratorRequest {
  idea: string;
}

export interface StoreGeneratorResponse {
  store: {
    name: string;
    description: string;
    tagline: string;
  };
  categories: Array<{
    name: string;
    description: string;
  }>;
  sample_products: Array<{
    name: string;
    description: string;
    price: number;
    category: string;
  }>;
  tokens_used?: number;
  mode: 'groq' | 'mock';
  processing_time?: number;
  success: boolean;
}

export interface AutomatedStoreResponse {
  success: boolean;
  message: string;
  store: Store;
  categories: Category[];
  brand: Brand;
  products: Product[];
  summary: {
    total_categories: number;
    total_products: number;
    ai_mode: string;
  };
  next_steps: string[];
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  user_type?: 'customer' | 'vendor';
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}
