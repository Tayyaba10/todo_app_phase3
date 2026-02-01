'use client';

import React from 'react';
import { Task } from '../../types';
import { useRouter } from 'next/dist/client/components/navigation';

interface TaskCardProps {
  task: Task;
  onToggle?: (id: string, completed: boolean) => void;
  // onEdit?: (task: Task) => void;
  onDelete?: (id: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggle, onDelete }) => {
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
    <div className={`border rounded-lg shadow-md p-4 ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      <div className="flex justify-between items-start">
        <div>
          <h3 className={`font-bold text-lg mb-2 ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-gray-600 mb-3 ${task.completed ? 'line-through' : ''}`}>
              {task.description}
            </p>
          )}
        </div>
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggle}
          className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 mt-1"
        />
      </div>
      <div className="flex justify-end space-x-2">
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

export default TaskCard;