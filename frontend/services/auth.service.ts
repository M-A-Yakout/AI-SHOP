import apiClient, { handleApiError } from '@/lib/api';
import { AuthResponse, LoginRequest, RegisterRequest, User } from '@/types';

export const authService = {
  async login(data: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>('/auth/login/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async register(data: RegisterRequest): Promise<AuthResponse> {
    try {
      // First register the user
      const registerData = {
        ...data,
        password2: data.password, // Add password confirmation
      };
      
      const registerResponse = await apiClient.post('/auth/register/', registerData);
      
      // Then login to get tokens
      const loginResponse = await apiClient.post<AuthResponse>('/auth/login/', {
        username: data.username,
        password: data.password,
      });
      
      return loginResponse.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getProfile(): Promise<User> {
    try {
      const response = await apiClient.get<User>('/auth/profile/');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    try {
      const response = await apiClient.put<User>('/auth/profile/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  logout() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  },
};
