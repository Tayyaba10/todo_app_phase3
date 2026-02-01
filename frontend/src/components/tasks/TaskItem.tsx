'use client';

import React from 'react';
import { Task } from '../../types';
import { useRouter } from 'next/dist/client/components/navigation';

interface TaskItemProps {
  task: Task;
  onToggle?: (id: string, completed: boolean) => void;
  // onEdit?: (task: Task) => void;
  onDelete?: (id: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete }) => {
  const handleToggle = () => {
    onToggle?.(task.id, !task.completed);
  };

  const router = useRouter();
  const handleEdit = () => {
    router.push(`/tasks/${task.id}/edit`);
  };

  const handleDelete = () => {
    onDelete?.(task.id);
  };

  return (
    <div className={`flex items-center justify-between p-4 mb-2 border rounded-lg ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      <div className="flex items-center">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggle}
          className="mr-3 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
        />
        <div>
          <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-sm ${task.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
        </div>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={handleEdit}
          className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskItem;