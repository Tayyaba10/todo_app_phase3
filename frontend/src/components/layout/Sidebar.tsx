'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../../lib/auth/auth-context';

const Sidebar: React.FC = () => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return null; // Don't show sidebar for non-authenticated users
  }

  return (
    <aside className="w-64 bg-gray-800 text-white min-h-screen p-4">
      <div className="mb-8">
        <h2 className="text-xl font-bold">Todo App</h2>
      </div>

      <nav>
        <ul className="space-y-2">
          <li>
            <Link
              href="/dashboard"
              className="block py-2 px-4 rounded hover:bg-gray-700 transition-colors"
            >
              Dashboard
            </Link>
          </li>
          <li>
            <Link
              href="/tasks"
              className="block py-2 px-4 rounded hover:bg-gray-700 transition-colors"
            >
              My Tasks
            </Link>
          </li>
          <li>
            <Link
              href="/tasks/create"
              className="block py-2 px-4 rounded hover:bg-gray-700 transition-colors"
            >
              Create Task
            </Link>
          </li>
          <li>
            <Link
              href="#"
              className="block py-2 px-4 rounded hover:bg-gray-700 transition-colors"
            >
              Profile
            </Link>
          </li>
          <li>
            <Link
              href="#"
              className="block py-2 px-4 rounded hover:bg-gray-700 transition-colors"
            >
              Settings
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;