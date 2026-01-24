import { Task } from '@/types';
import { getToken, removeToken } from '../auth/jwt-utils';

class ApiService {
  private baseUrl: string;

  constructor() {
    // Use NEXT_PUBLIC_API_BASE_URL which matches your .env.local
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api';
  }

  // Generic request method with auth token handling
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    // Get token if available
    const token = getToken();

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const config: RequestInit = {
      ...options,
      headers,
    };

    try {
      const url = `${this.baseUrl}${endpoint}`;
      const response = await fetch(url, config);

      // If response is 401, remove token and redirect to login
      if (response.status === 401) {
        removeToken();
        // In a Next.js app, you might want to redirect to login
        // This would typically be handled by the calling component
        throw new Error('Unauthorized: Please log in again');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      // Check if it's a network error (Failed to fetch)
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to reach the server. Please check if the backend is running.');
      }
      throw error;
    }
  }

  // Authentication methods
  async register(userData: { email: string; password: string; name?: string }) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials: { email: string; password: string }) {
    return this.request('/api/auth/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async getProfile() {
    return this.request('/api/auth/auth/profile');
  }

  // Task-related methods
  async getTasks() {
    return this.request('/tasks/');
  }

  async createTask(taskData: { title: string; description?: string }) {
    return this.request('/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  // async updateTask(taskId: number, taskData: { title?: string; description?: string; completed?: boolean }) {
  //   return this.request(`/tasks/${taskId}`, {
  //     method: 'PUT',
  //     body: JSON.stringify(taskData),
  //   });
  // }
  async getTaskById(taskId: number): Promise<Task> {
    return this.request<Task>(`/tasks/api/tasks/${taskId}`);
}
  async deleteTask(taskId: number) {
    return this.request(`/tasks/api/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(taskId: number, completed: boolean) {
    return this.request(`/tasks/api/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }
}

export const apiService = new ApiService();