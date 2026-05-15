import apiClient, { handleApiError } from '@/lib/api';
import { Order } from '@/types';

export const orderService = {
  async getOrders(params?: any): Promise<Order[]> {
    try {
      const response = await apiClient.get('/orders/', { params });
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

  async getOrder(id: number): Promise<Order> {
    try {
      const response = await apiClient.get<Order>(`/orders/${id}/`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createOrder(data: Partial<Order>): Promise<Order> {
    try {
      const response = await apiClient.post<Order>('/orders/create/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async updateOrder(id: number, data: Partial<Order>): Promise<Order> {
    try {
      const response = await apiClient.patch<Order>(`/orders/${id}/`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
