'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../../src/lib/hooks/useAuth';
import { useNotification } from '../../../src/lib/contexts/notification-context';
import { apiService } from '../../../src/lib/services/api';
import { TaskFormData } from '../../../src/types';
import TaskForm from '../../../src/components/tasks/TaskForm';
import ProtectedRoute from '../../../src/components/auth/ProtectedRoute';
import AuthenticatedLayout from '../../../src/components/layout/AuthenticatedLayout';

const CreateTaskPage = () => {
  const router = useRouter();
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (data: TaskFormData) => {
    try {
      setIsSubmitting(true);
      await apiService.createTask(data);
      showNotification('success', 'Task created successfully');
      router.push('/tasks');
      router.refresh(); // Refresh to show the new task
    } catch (err) {
      showNotification('error', (err as Error).message || 'Failed to create task');
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    router.back();
  };

  return (
    <ProtectedRoute>
      <AuthenticatedLayout>
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Create New Task</h1>

          <TaskForm
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            submitText={isSubmitting ? 'Creating...' : 'Create Task'}
          />
        </div>
      </AuthenticatedLayout>
    </ProtectedRoute>
  );
};

export default CreateTaskPage;