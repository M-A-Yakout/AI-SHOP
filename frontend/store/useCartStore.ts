import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartItem {
  id: number;
  slug: string;
  name: string;
  price: number;
  quantity: number;
  stock_quantity: number;
  image?: string;
  store_name?: string;
}

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: number) => void;
  updateQuantity: (id: number, quantity: number) => void;
  clearCart: () => void;
  getTotalItems: () => number;
  getTotalPrice: () => number;
}

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (item) => {
        const items = get().items;
        const existingItem = items.find((i) => i.id === item.id);

        // Ensure price is a valid number
        let price = typeof item.price === 'string' ? parseFloat(item.price) : item.price;
        
        // If price is still invalid, don't add the item
        if (isNaN(price) || !isFinite(price) || price <= 0) {
          console.error('Invalid price for item:', item);
          return;
        }

        const normalizedItem = {
          ...item,
          price: price,
        };

        if (existingItem) {
          // Update quantity if item already exists
          set({
            items: items.map((i) =>
              i.id === normalizedItem.id
                ? { ...i, quantity: Math.min(i.quantity + normalizedItem.quantity, i.stock_quantity) }
                : i
            ),
          });
        } else {
          // Add new item
          set({ items: [...items, normalizedItem] });
        }
      },

      removeItem: (id) => {
        set({ items: get().items.filter((i) => i.id !== id) });
      },

      updateQuantity: (id, quantity) => {
        if (quantity <= 0) {
          get().removeItem(id);
          return;
        }

        set({
          items: get().items.map((i) =>
            i.id === id ? { ...i, quantity: Math.min(quantity, i.stock_quantity) } : i
          ),
        });
      },

      clearCart: () => {
        set({ items: [] });
      },

      getTotalItems: () => {
        return get().items.reduce((total, item) => total + item.quantity, 0);
      },

      getTotalPrice: () => {
        return get().items.reduce((total, item) => {
          const price = typeof item.price === 'string' ? parseFloat(item.price) : item.price;
          if (isNaN(price) || !isFinite(price)) {
            return total;
          }
          return total + (price * item.quantity);
        }, 0);
      },
    }),
    {
      name: 'cart-storage',
      version: 2, // Increment version to force migration
      // Migrate old data with string prices to number prices
      migrate: (persistedState: any, version: number) => {
        // If version is less than 2, clear the cart (corrupted data)
        if (version < 2) {
          console.log('Clearing old cart data due to version upgrade');
          return { items: [] };
        }
        
        if (persistedState && persistedState.items) {
          // Filter out items with invalid prices
          persistedState.items = persistedState.items
            .map((item: any) => {
              const price = typeof item.price === 'string' ? parseFloat(item.price) : item.price;
              return {
                ...item,
                price: price,
              };
            })
            .filter((item: any) => {
              const isValid = !isNaN(item.price) && isFinite(item.price) && item.price > 0;
              if (!isValid) {
                console.log('Removing invalid item from cart:', item);
              }
              return isValid;
            });
        }
        return persistedState;
      },
    }
  )
);
