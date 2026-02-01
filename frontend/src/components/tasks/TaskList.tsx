'use client';

import React from 'react';
import { Task } from '../../types';
import TaskItem from './TaskItem';
import TaskCard from './TaskCard';
import Skeleton from '../ui/Skeleton';

interface TaskListProps {
  tasks: Task[];
  viewMode?: 'list' | 'grid';
  loading?: boolean;
  onToggle?: (id: string, completed: boolean) => void;
  // onEdit?: (task: Task) => void;
  onDelete?: (id: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  viewMode = 'list',
  loading = false,
  onToggle,
  // onEdit,
  onDelete
}) => {
  if (loading) {
    // Show skeleton loading state
    return (
      <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-2'}>
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} className="border rounded-lg p-4 bg-white">
            <Skeleton className="h-6 w-3/4 mb-2" />
            <Skeleton className="h-4 w-full mb-1" />
            <Skeleton className="h-4 w-2/3" />
          </div>
        ))}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No tasks found. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-2'}>
      {tasks.map(task => (
        viewMode === 'list' ? (
          <TaskItem
            key={task.id}
            task={task}
            onToggle={onToggle}
            // onEdit={onEdit}
            onDelete={onDelete}
          />
        ) : (
          <TaskCard
            key={task.id}
            task={task}
            onToggle={onToggle}
            // onEdit={onEdit}
            onDelete={onDelete}
          />
        )
      ))}
    </div>
  );
};

export default TaskList;