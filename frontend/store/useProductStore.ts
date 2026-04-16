import { create } from 'zustand';
import { Product, Category, Brand } from '@/types';

interface ProductState {
  products: Product[];
  categories: Category[];
  brands: Brand[];
  selectedProduct: Product | null;
  setProducts: (products: Product[]) => void;
  setCategories: (categories: Category[]) => void;
  setBrands: (brands: Brand[]) => void;
  setSelectedProduct: (product: Product | null) => void;
  addProduct: (product: Product) => void;
  updateProduct: (slug: string, product: Product) => void;
  removeProduct: (slug: string) => void;
}

export const useProductStore = create<ProductState>((set) => ({
  products: [],
  categories: [],
  brands: [],
  selectedProduct: null,
  setProducts: (products) => set({ products }),
  setCategories: (categories) => set({ categories }),
  setBrands: (brands) => set({ brands }),
  setSelectedProduct: (product) => set({ selectedProduct: product }),
  addProduct: (product) => set((state) => ({ products: [...state.products, product] })),
  updateProduct: (slug, product) =>
    set((state) => ({
      products: state.products.map((p) => (p.slug === slug ? product : p)),
    })),
  removeProduct: (slug) =>
    set((state) => ({
      products: state.products.filter((p) => p.slug !== slug),
    })),
}));
