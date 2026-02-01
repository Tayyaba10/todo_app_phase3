import unittest
from unittest.mock import patch, MagicMock

# Test to verify the API service fixes work correctly
class TestApiService(unittest.TestCase):

    def setUp(self):
        # Import the ApiService class after our changes
        from frontend.src.lib.services.api import ApiService

        # Create a mock environment
        import os
        os.environ['NEXT_PUBLIC_API_BASE_URL'] = 'http://127.0.0.1:8000'

        self.api_service = ApiService()

    def test_base_url_configuration(self):
        """Test that the base URL is correctly configured"""
        # The base URL should be http://127.0.0.1:8000 (without /api)
        expected_base_url = 'http://127.0.0.1:8000'
        self.assertEqual(self.api_service.base_url, expected_base_url)

    def test_send_message_endpoint(self):
        """Test that the sendMessage method constructs the correct endpoint"""
        # Import the method we want to test
        with patch.object(self.api_service, 'request') as mock_request:
            user_id = '123e4567-e89b-12d3-a456-426614174000'
            message = 'Test message'

            # Call the method
            self.api_service.sendMessage(user_id, message)

            # Verify that the request method was called with the correct endpoint
            # Should be /api/{user_id}/chat to match backend route structure
            expected_endpoint = f'/api/{user_id}/chat'
            mock_request.assert_called_once()

            # Get the actual call
            actual_call_args = mock_request.call_args
            actual_endpoint = actual_call_args[0][0]  # First positional argument

            self.assertEqual(actual_endpoint, expected_endpoint)

    def test_task_endpoints_include_api_prefix(self):
        """Test that task endpoints now include the /api prefix"""
        with patch.object(self.api_service, 'request') as mock_request:
            # Test getTasks
            self.api_service.getTasks()
            mock_request.assert_called_with('/api/tasks/')

            # Reset mock and test createTask
            mock_request.reset_mock()
            task_data = {'title': 'Test task'}
            self.api_service.createTask(task_data)
            mock_request.assert_called_with('/api/tasks/', method='POST', body=unittest.mock.ANY)

if __name__ == '__main__':
    unittest.main()