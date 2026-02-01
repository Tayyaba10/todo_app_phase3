'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../lib/auth/auth-context';
import { useNotification } from '../../lib/contexts/notification-context';
import { apiService } from '../../lib/services/api';
import { Task } from '../../types';
import TaskList from '../../components/tasks/TaskList';
import Link from 'next/link';
import ProtectedRoute from '../../components/auth/ProtectedRoute';
import AuthenticatedLayout from '../../components/layout/AuthenticatedLayout';

const TasksPage = () => {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await apiService.getTasks();

    const tasksArray: Task[] = Array.isArray(response.tasks)
      ? response.tasks
      : [];

    setTasks(tasksArray);
  } catch (err) {
    showNotification(
      'error',
      (err as Error).message || 'Failed to fetch tasks'
    );
    setTasks([]); // ✅ fallback safety
  } finally {
    setLoading(false);
  }
  };

  const handleToggleTask = async (id: string, completed: boolean) => {
    try {
      await apiService.toggleTaskCompletion(id, completed);
      setTasks(tasks.map(task =>
        task.id === id ? { ...task, completed } : task
      ));
      showNotification('success', `Task ${completed ? 'completed' : 'marked as incomplete'}`);
    } catch (err) {
      showNotification('error', (err as Error).message || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await apiService.deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
      showNotification('success', 'Task deleted successfully');
    } catch (err) {
      showNotification('error', (err as Error).message || 'Failed to delete task');
    }
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <AuthenticatedLayout>
          <div className="flex justify-center items-center min-h-[60vh]">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        </AuthenticatedLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AuthenticatedLayout>
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <Link
            href="/tasks/create"
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Create Task
          </Link>
        </div>

        <TaskList
          tasks={tasks}
          viewMode="list"
          loading={false}
          onToggle={handleToggleTask}
          onDelete={handleDeleteTask}
        />
      </AuthenticatedLayout>
    </ProtectedRoute>
  );
};

export default TasksPage;