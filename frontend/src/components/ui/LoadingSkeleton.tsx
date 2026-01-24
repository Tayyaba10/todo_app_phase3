import React from 'react';

interface LoadingSkeletonProps {
  type?: 'card' | 'list-item' | 'text' | 'avatar' | 'button';
  count?: number;
  className?: string;
}

const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  type = 'card',
  count = 1,
  className = ''
}) => {
  const baseClasses = 'animate-pulse bg-gray-200 rounded-md';

  const getDimensions = () => {
    switch (type) {
      case 'card':
        return 'h-32';
      case 'list-item':
        return 'h-16';
      case 'text':
        return 'h-4';
      case 'avatar':
        return 'h-10 w-10 rounded-full';
      case 'button':
        return 'h-10 w-24';
      default:
        return 'h-32';
    }
  };

  const skeletons = Array.from({ length: count }, (_, index) => (
    <div
      key={index}
      className={`${baseClasses} ${getDimensions()} ${className}`}
      aria-label="Loading content"
    />
  ));

  return <>{skeletons}</>;
};

export default LoadingSkeleton;