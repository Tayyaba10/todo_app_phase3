import React from 'react';

interface SkeletonProps {
  className?: string;
  count?: number;
}

const Skeleton: React.FC<SkeletonProps> = ({
  className = 'h-4 w-full',
  count = 1
}) => {
  const skeletons = Array.from({ length: count }, (_, index) => (
    <div
      key={index}
      className={`animate-pulse bg-gray-200 rounded-md ${className}`}
      role="status"
      aria-label="Loading content"
    />
  ));

  return <>{skeletons}</>;
};

export default Skeleton;