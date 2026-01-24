'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useAuth as useAuthContext } from '../auth/auth-context';

/**
 * Enhanced useAuth hook that provides authentication functionality
 * and navigation logic for auth redirects
 */
export const useAuth = () => {
  const authContext = useAuthContext();
  const router = useRouter();

  /**
   * Redirect to login if not authenticated
   */
  const requireAuth = (redirectPath: string = '/login') => {
    useEffect(() => {
      if (!authContext.loading && !authContext.isAuthenticated) {
        router.push(redirectPath);
      }
    }, [authContext.isAuthenticated, authContext.loading, redirectPath, router]);
  };

  /**
   * Redirect to dashboard if already authenticated (for login/register pages)
   */
  const redirectIfAuthenticated = (redirectPath: string = '/dashboard') => {
    useEffect(() => {
      if (!authContext.loading && authContext.isAuthenticated) {
        router.push(redirectPath);
      }
    }, [authContext.isAuthenticated, authContext.loading, redirectPath, router]);
  };

  return {
    ...authContext,
    requireAuth,
    redirectIfAuthenticated,
  };
};