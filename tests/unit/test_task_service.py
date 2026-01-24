import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from backend.src.models.task import Task, TaskCreate
from backend.src.services.task_service import TaskService


class TestTaskService:
    """Unit tests for TaskService"""

    def test_create_task(self):
        """Test creating a new task"""
        session = Mock(spec=Session)

        task_create = TaskCreate(title="Test Task", description="Test Description", completed=False)
        user_id = 1

        # Mock the session behavior
        mock_task = Task(id=1, title="Test Task", description="Test Description", completed=False, user_id=1)
        session.add = Mock()
        session.commit = Mock()
        session.refresh = Mock(side_effect=lambda obj: setattr(obj, 'id', 1))

        with patch.object(Task, '__init__', return_value=None):
            result = TaskService.create_task(session, task_create, user_id)

            assert session.add.called
            assert session.commit.called
            assert session.refresh.called

    def test_get_task_by_id_success(self):
        """Test getting a task by ID successfully"""
        session = Mock(spec=Session)

        # Create a mock task
        mock_task = Mock()
        mock_task.id = 1
        mock_task.user_id = 1
        mock_task.title = "Test Task"

        # Mock the exec method to return the task
        exec_mock = Mock()
        exec_mock.first.return_value = mock_task
        session.exec.return_value = exec_mock

        result = TaskService.get_task_by_id(session, 1, 1)

        assert result == mock_task
        session.exec.assert_called_once()

    def test_get_task_by_id_not_found(self):
        """Test getting a task by ID that doesn't exist"""
        from backend.src.core.exceptions import TaskNotFoundException
        session = Mock(spec=Session)

        # Mock the exec method to return None
        exec_mock = Mock()
        exec_mock.first.return_value = None
        session.exec.return_value = exec_mock

        with pytest.raises(TaskNotFoundException):
            TaskService.get_task_by_id(session, 999, 1)

    def test_get_tasks_by_user(self):
        """Test getting all tasks for a user"""
        session = Mock(spec=Session)

        # Create mock tasks
        mock_task1 = Mock()
        mock_task1.id = 1
        mock_task1.user_id = 1
        mock_task1.title = "Task 1"

        mock_task2 = Mock()
        mock_task2.id = 2
        mock_task2.user_id = 1
        mock_task2.title = "Task 2"

        mock_tasks = [mock_task1, mock_task2]

        # Mock the exec method to return the tasks
        exec_mock = Mock()
        exec_mock.all.return_value = mock_tasks
        session.exec.return_value = exec_mock

        result = TaskService.get_tasks_by_user(session, 1)

        assert len(result) == 2
        assert result == mock_tasks
        session.exec.assert_called_once()

    def test_update_task_success(self):
        """Test updating a task successfully"""
        session = Mock(spec=Session)

        # Create a mock task
        mock_task = Mock()
        mock_task.id = 1
        mock_task.user_id = 1
        mock_task.title = "Old Title"

        # Mock the exec method to return the task
        exec_mock = Mock()
        exec_mock.first.return_value = mock_task
        session.exec.return_value = exec_mock

        # Create update data
        from backend.src.models.task import TaskUpdate
        task_update = TaskUpdate(title="New Title")

        result = TaskService.update_task(session, 1, task_update, 1)

        assert result == mock_task
        assert mock_task.title == "New Title"  # Updated attribute
        session.add.assert_called_once()
        session.commit.assert_called_once()

    def test_delete_task_success(self):
        """Test deleting a task successfully"""
        session = Mock(spec=Session)

        # Create a mock task
        mock_task = Mock()
        mock_task.id = 1
        mock_task.user_id = 1

        # Mock the exec method to return the task
        exec_mock = Mock()
        exec_mock.first.return_value = mock_task
        session.exec.return_value = exec_mock

        result = TaskService.delete_task(session, 1, 1)

        assert result is True
        session.delete.assert_called_once_with(mock_task)
        session.commit.assert_called_once()

    def test_toggle_task_completion(self):
        """Test toggling task completion status"""
        session = Mock(spec=Session)

        # Create a mock task with completed=False
        mock_task = Mock()
        mock_task.id = 1
        mock_task.user_id = 1
        mock_task.completed = False

        # Mock the exec method to return the task
        exec_mock = Mock()
        exec_mock.first.return_value = mock_task
        session.exec.return_value = exec_mock

        result = TaskService.toggle_task_completion(session, 1, 1)

        # The task should now be completed=True
        assert mock_task.completed is True
        session.add.assert_called_once()
        session.commit.assert_called_once()