'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuth } from '../../../../lib/auth/auth-context';
import { useNotification } from '../../../../lib/contexts/notification-context';
import { apiService } from '../../../../lib/services/api';
import { Task, TaskFormData } from '../../../../types';
import TaskForm from '../../../../components/tasks/TaskForm';
import ProtectedRoute from '../../../../components/auth/ProtectedRoute';
import AuthenticatedLayout from '../../../../components/layout/AuthenticatedLayout';

const EditTaskPage = () => {
  const router = useRouter();
  const params = useParams();
  const taskId = params.id as string;
  const { user } = useAuth();
  const { showNotification } = useNotification();

  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetchTask();
  }, [taskId]);

  const fetchTask = async () => {
    try {
      setLoading(true);
      // const data = await apiService.getTasks();
      // const tasksArray: Task[] = Array.isArray(data) ? data : (data.data || []);
      // const foundTask = tasksArray.find(t => t.id === taskId);

      const foundTask = await apiService.getTaskById(taskId); // ✅ direct call
      setTask(foundTask);
    } catch (err) {
      showNotification('error', (err as Error).message || 'Failed to fetch task');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (data: TaskFormData) => {
    try {
      setIsSubmitting(true);
      await apiService.updateTask(taskId.toString(), data);
      showNotification('success', 'Task updated successfully');
      router.push('/tasks');
      router.refresh(); // Refresh to show the updated task
    } catch (err) {
      showNotification('error', (err as Error).message || 'Failed to update task');
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    router.back();
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="container mx-auto px-4 py-8 flex justify-center items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      </ProtectedRoute>
    );
  }

  if (error) {
    return (
      <ProtectedRoute>
        <div className="container mx-auto px-4 py-8">
          <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            Error: {error}
          </div>
          <button
            onClick={() => router.back()}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Back to Tasks
          </button>
        </div>
      </ProtectedRoute>
    );
  }

  if (!task) {
    return (
      <ProtectedRoute>
        <div className="container mx-auto px-4 py-8">
          <div className="p-4 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded">
            Task not found
          </div>
          <button
            onClick={() => router.back()}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Back to Tasks
          </button>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AuthenticatedLayout>
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Edit Task</h1>

          <TaskForm
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            initialData={{
              title: task.title,
              description: task.description || ''
            }}
            submitText={isSubmitting ? 'Updating...' : 'Update Task'}
          />
        </div>
      </AuthenticatedLayout>
    </ProtectedRoute>
  );
};

export default EditTaskPage;