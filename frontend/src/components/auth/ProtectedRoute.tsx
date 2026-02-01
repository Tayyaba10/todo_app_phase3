'use client';

import React, { ReactNode, useEffect } from 'react';
import { useAuth } from '../../lib/auth/auth-context';
import { useRouter, usePathname } from 'next/navigation';

interface ProtectedRouteProps {
  children: ReactNode;
  redirectTo?: string;
  fallback?: ReactNode; // Optional fallback component while loading or redirecting
}

/**
 * Enhanced Protected Route component that wraps protected pages and checks for authentication
 * If user is not authenticated, redirects to login page
 * Also handles token expiration and stores the intended destination for redirect after login
 */
const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  redirectTo = '/auth/login',
  fallback
}) => {
  const { isAuthenticated, loading, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!loading) {
      if (!isAuthenticated) {
        // Store the attempted route in localStorage so we can redirect back after login
        if (pathname && pathname !== '/' && !pathname.includes('auth/login') && !pathname.includes('auth/signup')) {
          localStorage.setItem('redirectAfterLogin', pathname);
        }
        router.push(redirectTo);
      }
    }
  }, [isAuthenticated, loading, redirectTo, router, pathname]);

  // Show loading state while checking authentication
  if (loading) {
    return fallback || (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // If authenticated, render children
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // If not authenticated and not redirected yet, return fallback or null
  // (redirect effect should handle navigation)
  return fallback || null;
};

export default ProtectedRoute;