'use client';

import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { Task } from '../../types';

interface UseTasksReturn {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  fetchTasks: () => Promise<void>;
  createTask: (taskData: { title: string; description?: string }) => Promise<void>;
  updateTask: (id: number, taskData: { title?: string; description?: string; completed?: boolean }) => Promise<void>;
  deleteTask: (id: number) => Promise<void>;
  toggleTaskCompletion: (id: number, completed: boolean) => Promise<void>;
}

export const useTasks = (): UseTasksReturn => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getTasks();

      // Handle different response formats
      if (Array.isArray(response)) {
        setTasks(response);
      } else if (response.data && Array.isArray(response.data)) {
        setTasks(response.data);
      } else {
        setTasks([]);
      }
    } catch (err) {
      setError((err as Error).message || 'Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (taskData: { title: string; description?: string }) => {
    try {
      setError(null);
      const newTask = await apiService.createTask(taskData);

      // Handle different response formats
      const taskToAdd = newTask.id ? newTask : (newTask.data || {});
      if (taskToAdd.id) {
        setTasks(prev => [...prev, taskToAdd]);
      }
    } catch (err) {
      setError((err as Error).message || 'Failed to create task');
      console.error('Error creating task:', err);
      throw err;
    }
  };

  const updateTask = async (id: number, taskData: { title?: string; description?: string; completed?: boolean }) => {
    try {
      setError(null);
      const updatedTask = await apiService.updateTask(id, taskData);

      // Handle different response formats
      const taskToUpdate = updatedTask.id ? updatedTask : (updatedTask.data || {});
      setTasks(prev => prev.map(task => task.id === id ? { ...task, ...taskToUpdate } : task));
    } catch (err) {
      setError((err as Error).message || 'Failed to update task');
      console.error('Error updating task:', err);
      throw err;
    }
  };

  const deleteTask = async (id: number) => {
    try {
      setError(null);
      await apiService.deleteTask(id);
      setTasks(prev => prev.filter(task => task.id !== id));
    } catch (err) {
      setError((err as Error).message || 'Failed to delete task');
      console.error('Error deleting task:', err);
      throw err;
    }
  };

  const toggleTaskCompletion = async (id: number, completed: boolean) => {
    try {
      setError(null);
      const updatedTask = await apiService.toggleTaskCompletion(id, completed);

      // Handle different response formats
      const taskToUpdate = updatedTask.id ? updatedTask : (updatedTask.data || {});
      setTasks(prev => prev.map(task => task.id === id ? { ...task, completed: taskToUpdate.completed } : task));
    } catch (err) {
      setError((err as Error).message || 'Failed to toggle task completion');
      console.error('Error toggling task completion:', err);
      throw err;
    }
  };

  // Fetch tasks on mount
  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion
  };
};