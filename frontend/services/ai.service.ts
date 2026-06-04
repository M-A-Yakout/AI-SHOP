import apiClient, { handleApiError } from '@/lib/api';
import {
  ProductAssistRequest,
  ProductAssistResponse,
  StoreGeneratorRequest,
  StoreGeneratorResponse,
  AutomatedStoreResponse,
} from '@/types';

export const aiService = {
  // ===== Original Endpoints =====
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

  // ===== Enhanced Endpoints (NEW) =====
  
  // Conversations
  async createConversation(language = 'en', title = 'New Chat'): Promise<any> {
    try {
      const response = await apiClient.post('/ai/conversations/create/', { language, title });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async sendMessage(sessionId: number, message: string): Promise<any> {
    try {
      const response = await apiClient.post(`/ai/conversations/${sessionId}/send/`, { message });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getConversation(sessionId: number): Promise<any> {
    try {
      const response = await apiClient.get(`/ai/conversations/${sessionId}/`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async listConversations(): Promise<any> {
    try {
      const response = await apiClient.get('/ai/conversations/');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Recommendations
  async getRecommendations(language = 'en'): Promise<any> {
    try {
      const response = await apiClient.get('/ai/recommendations/', { params: { language } });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async recordRecommendationClick(recommendationId: number): Promise<any> {
    try {
      const response = await apiClient.post(`/ai/recommendations/${recommendationId}/click/`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Web Search
  async webSearch(query: string, language = 'en'): Promise<any> {
    try {
      const response = await apiClient.get('/ai/search/web/', {
        params: { q: query, language }
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Languages
  async getSupportedLanguages(): Promise<any> {
    try {
      const response = await apiClient.get('/ai/languages/');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async detectLanguage(text: string, targetLanguage = 'en'): Promise<any> {
    try {
      const response = await apiClient.post('/ai/languages/detect/', {
        text,
        target_language: targetLanguage
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Enhanced Product Assist
  async enhanceProductMultilingual(data: any): Promise<any> {
    try {
      const response = await apiClient.post('/ai/product-assist/multilingual/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ===== Intent-Based Methods =====

  async searchAndRecommend(query: string): Promise<any> {
    try {
      const response = await apiClient.post('/ai/search-and-recommend/', { query });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async generateProductNames(idea: string): Promise<any> {
    try {
      const response = await apiClient.post('/ai/generate-product-names/', { idea });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async generateStore(idea: string): Promise<any> {
    try {
      const response = await apiClient.post('/ai/create-automated-store/', { idea });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
