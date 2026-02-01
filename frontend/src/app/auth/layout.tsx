import React from 'react';

interface AuthLayoutProps {
  children: React.ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div>
      {/* Auth pages wrapper - can include common elements like headers/footers */}
      {children}
    </div>
  );
};

export default AuthLayout;