import apiClient, { handleApiError } from '@/lib/api';
import { Product, Category, Brand } from '@/types';

export const productService = {
  async getProducts(params?: any): Promise<Product[]> {
    try {
      const response = await apiClient.get('/products/', { params });
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

  async getProduct(slug: string): Promise<Product> {
    try {
      const response = await apiClient.get<Product>(`/products/${slug}/`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createProduct(data: Partial<Product>): Promise<Product> {
    try {
      const response = await apiClient.post<Product>('/products/create/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async updateProduct(slug: string, data: Partial<Product>): Promise<Product> {
    try {
      const response = await apiClient.put<Product>(`/products/${slug}/`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async deleteProduct(slug: string): Promise<void> {
    try {
      await apiClient.delete(`/products/${slug}/`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getCategories(): Promise<Category[]> {
    try {
      const response = await apiClient.get('/products/categories/');
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

  async getBrands(): Promise<Brand[]> {
    try {
      const response = await apiClient.get('/products/brands/');
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
};
