import { useAuthStore } from '../store/useAuthStore';

const BASE_URL = import.meta.env.VITE_API_URL || '';

export async function apiClient(endpoint, { method = 'GET', body, headers = {} } = {}) {
  const token = useAuthStore.getState().token;
  
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    }
  };

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  if (body) {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, config);
  
  if (!response.ok) {
    if (response.status === 401) {
      useAuthStore.getState().logout();
    }
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'API request failed');
  }
  
  return response.json();
}
