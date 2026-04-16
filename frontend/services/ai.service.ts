import apiClient, { handleApiError } from '@/lib/api';
import {
  ProductAssistRequest,
  ProductAssistResponse,
  StoreGeneratorRequest,
  StoreGeneratorResponse,
  AutomatedStoreResponse,
} from '@/types';

export const aiService = {
  async enhanceProduct(data: ProductAssistRequest): Promise<ProductAssistResponse> {
    try {
      const response = await apiClient.post<ProductAssistResponse>('/ai/product-assist/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async generateStore(data: StoreGeneratorRequest): Promise<StoreGeneratorResponse> {
    try {
      const response = await apiClient.post<StoreGeneratorResponse>('/ai/store-generator/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createAutomatedStore(idea: string): Promise<AutomatedStoreResponse> {
    try {
      const response = await apiClient.post<AutomatedStoreResponse>('/ai/create-automated-store/', { idea });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getUsageStats(): Promise<any> {
    try {
      const response = await apiClient.get('/ai/usage-stats/');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
