import { Task } from '@/types';
import { getToken, removeToken } from '../auth/jwt-utils';

class ApiService {
  private baseUrl: string;

  constructor() {
    // Use NEXT_PUBLIC_API_BASE_URL which matches your .env.local
    // The base URL should NOT include /api since individual routes add their own prefixes
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
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

      const responseData = await response.json();

      // Transform response data to match frontend type expectations
      // Backend uses snake_case (user_id) but frontend expects camelCase (userId)
      if (endpoint.includes('/api/tasks')) {
        return this.transformTaskResponse(responseData) as T;
      }

      return responseData;
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      // Check if it's a network error (Failed to fetch)
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to reach the server. Please check if the backend is running.');
      }
      throw error;
    }
  }

  // Transform task response to match frontend type expectations
  private transformTaskResponse(data: any) {
    if (!data) return data;

    // If it's a task list response
    if (data.tasks && Array.isArray(data.tasks)) {
      return {
        ...data,
        tasks: data.tasks.map(this.transformSingleTask)
      };
    }

    // If it's a single task response
    if (data.hasOwnProperty('user_id')) {
      return this.transformSingleTask(data);
    }

    return data;
  }

  private transformSingleTask(task: any) {
    if (!task) return task;

    return {
      ...task,
      userId: task.user_id || task.userId,
      createdAt: task.created_at || task.createdAt,
      updatedAt: task.updated_at || task.updatedAt
    };
  }

  // Authentication methods
  async register(userData: { email: string; password: string; name?: string }) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials: { email: string; password: string }) {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async getProfile() {
    return this.request('/api/auth/profile');
  }

  // Task-related methods
  async getTasks() {
    return this.request('/api/tasks/');
  }

  async createTask(taskData: { title: string; description?: string }) {
    return this.request('/api/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(taskId: string, taskData: { title?: string; description?: string; completed?: boolean }) {
    return this.request(`/api/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async getTaskById(taskId: string): Promise<Task> {
    return this.request<Task>(`/api/tasks/${taskId}`);
  }

  async deleteTask(taskId: string) {
    return this.request(`/api/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(taskId: string, completed: boolean) {
    return this.request(`/api/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }

  // Chat-related methods
  // 
  // Chat-related methods
async sendMessage(userId: string, message: string, conversationId?: string) {
  console.log('=== sendMessage called ===');
  console.log('User ID:', userId);
  console.log('Message:', message);
  console.log('Base URL:', this.baseUrl);
  
  if (!userId) {
    throw new Error('User ID is required to send a chat message');
  }

  const bodyData: any = { message };
  if (conversationId) {
    bodyData.conversation_id = conversationId;
  }

  console.log('Request body:', bodyData);
  console.log('Endpoint:', `/api/chat/${userId}`);

  return this.request(`/api/chat/${userId}`, {  // ✅ CHANGE THIS LINE
    method: 'POST',
    body: JSON.stringify(bodyData),
  });
}
}

export const apiService = new ApiService();
