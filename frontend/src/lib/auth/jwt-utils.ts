/**
 * JWT utilities for frontend token management
 */

// Store token in localStorage
export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token);
  }
};

// Get token from localStorage
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
};

// Remove token from localStorage
export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
  }
};

// Check if token exists
export const hasToken = (): boolean => {
  return getToken() !== null;
};

// Decode JWT token to get payload
export const decodeToken = (token: string): any | null => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

// Check if token is expired
export const isTokenExpired = (token: string): boolean => {
  const payload = decodeToken(token);
  if (!payload || !payload.exp) {
    return true; // Consider invalid tokens as expired
  }

  const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
  return payload.exp < currentTime;
};

// Check if token will expire soon (within 5 minutes)
export const isTokenExpiringSoon = (token: string, thresholdSeconds: number = 300): boolean => {
  const payload = decodeToken(token);
  if (!payload || !payload.exp) {
    return true; // Consider invalid tokens as expiring soon
  }

  const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
  return payload.exp - currentTime < thresholdSeconds;
};

// Get token expiration time
export const getTokenExpiration = (token: string): number | null => {
  const payload = decodeToken(token);
  if (!payload || !payload.exp) {
    return null;
  }
  return payload.exp;
};

// Get time until token expires in seconds
export const getTimeUntilExpiration = (token: string): number | null => {
  const payload = decodeToken(token);
  if (!payload || !payload.exp) {
    return null;
  }

  const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
  return payload.exp - currentTime;
};