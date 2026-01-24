'use client';

import React, { ReactNode } from 'react';
import { AuthProvider as BaseAuthProvider } from './auth-context';

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Authentication Provider wrapper that sets up the authentication context
 * for the entire application.
 */
const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  return <BaseAuthProvider>{children}</BaseAuthProvider>;
};

export default AuthProvider;