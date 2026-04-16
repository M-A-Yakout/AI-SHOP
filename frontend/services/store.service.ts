import apiClient, { handleApiError } from '@/lib/api';
import { Store } from '@/types';

export const storeService = {
  async getStores(params?: any): Promise<Store[]> {
    try {
      const response = await apiClient.get('/stores/', { params });
      // Handle both paginated and non-paginated responses
      const data = response.data;
      if (Array.isArray(data)) {
        return data;
      } else if (data.results && Array.isArray(data.results)) {
        return data.results;
      }
      return [];
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getMyStores(): Promise<Store[]> {
    try {
      const response = await apiClient.get('/stores/my-stores/');
      // Handle both paginated and non-paginated responses
      const data = response.data;
      if (Array.isArray(data)) {
        return data;
      } else if (data.results && Array.isArray(data.results)) {
        return data.results;
      }
      return [];
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getStore(slug: string): Promise<Store> {
    try {
      const response = await apiClient.get<Store>(`/stores/${slug}/`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createStore(data: Partial<Store>): Promise<Store> {
    try {
      const response = await apiClient.post<Store>('/stores/create/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async updateStore(slug: string, data: Partial<Store>): Promise<Store> {
    try {
      const response = await apiClient.put<Store>(`/stores/${slug}/`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async deleteStore(slug: string): Promise<void> {
    try {
      await apiClient.delete(`/stores/${slug}/`);
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
