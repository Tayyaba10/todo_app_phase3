'use client';

import React from 'react';
import Link from 'next/link';
import ProtectedRoute from '../../components/auth/ProtectedRoute';
import AuthenticatedLayout from '../../components/layout/AuthenticatedLayout';

const DashboardPage = () => {
  return (
    <ProtectedRoute>
      <AuthenticatedLayout>
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link href="/tasks" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">My Tasks</h2>
            <p className="text-gray-600">View and manage your tasks</p>
          </Link>

          <Link href="/tasks/create" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Create Task</h2>
            <p className="text-gray-600">Add a new task to your list</p>
          </Link>

          <Link href="/chat" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">AI Chat Assistant</h2>
            <p className="text-gray-600">Manage tasks with natural language</p>
          </Link>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Statistics</h2>
            <p className="text-gray-600">Coming soon...</p>
          </div>
        </div>
      </AuthenticatedLayout>
    </ProtectedRoute>
  );
};

export default DashboardPage;