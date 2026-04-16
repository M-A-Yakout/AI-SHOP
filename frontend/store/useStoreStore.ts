import { create } from 'zustand';
import { Store } from '@/types';

interface StoreState {
  stores: Store[];
  selectedStore: Store | null;
  setStores: (stores: Store[]) => void;
  setSelectedStore: (store: Store | null) => void;
  addStore: (store: Store) => void;
  updateStore: (slug: string, store: Store) => void;
  removeStore: (slug: string) => void;
}

export const useStoreStore = create<StoreState>((set) => ({
  stores: [],
  selectedStore: null,
  setStores: (stores) => set({ stores }),
  setSelectedStore: (store) => set({ selectedStore: store }),
  addStore: (store) => set((state) => ({ stores: [...state.stores, store] })),
  updateStore: (slug, store) =>
    set((state) => ({
      stores: state.stores.map((s) => (s.slug === slug ? store : s)),
    })),
  removeStore: (slug) =>
    set((state) => ({
      stores: state.stores.filter((s) => s.slug !== slug),
    })),
}));
