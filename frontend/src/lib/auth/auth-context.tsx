'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { signIn as betterSignIn, signOut as betterSignOut, useSession as betterUseSession } from './better-auth-client';
import { setToken, getToken, removeToken, decodeToken, isTokenExpired, isTokenExpiringSoon } from './jwt-utils';
import { apiService } from '../services/api';

interface AuthContextType {
  user: any;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [token, setTokenState] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Check for existing token on initial load
  useEffect(() => {
    const storedToken = getToken();
    if (storedToken && !isTokenExpired(storedToken)) {
      setTokenState(storedToken);
    } else {
      removeToken();
    }
    setLoading(false);
  }, []);

  // Check for token expiration periodically
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    if (token && !isTokenExpired(token)) {
      // Check every minute if token is expiring soon
      interval = setInterval(() => {
        if (token && isTokenExpiringSoon(token, 60)) { // Logout 1 minute before expiration
          console.warn('Token expiring soon, logging out...');
          handleTokenExpiration();
        }
      }, 60000); // Check every minute
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [token]);

  const handleTokenExpiration = () => {
    removeToken();
    setTokenState(null);
  };

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await apiService.login({ email, password });

      if (response && response.token) {
        setToken(response.token);
        setTokenState(response.token);
      } else {
        throw new Error('Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await apiService.register({ email, password, name: email.split('@')[0] }); // Use part of email as name

      if (response && response.token) {
        setToken(response.token);
        setTokenState(response.token);
      } else {
        throw new Error('Registration failed');
      }
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      // Clear token from storage and state
      removeToken();
      setTokenState(null);

      // Call Better Auth sign out
      await betterSignOut();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setLoading(false);
    }
  };

  const isAuthenticated = !!token && !isTokenExpired(token);

  // Get user info from token if authenticated
  const user = token && !isTokenExpired(token) ? decodeToken(token) : null;

  const value: AuthContextType = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};