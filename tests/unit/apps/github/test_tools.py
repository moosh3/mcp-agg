import unittest
from unittest.mock import Mock, patch

from api.apps.github.tools import GitHubToolHandler, create_github_handler, GITHUB_TOOLS


class TestGitHubTools(unittest.TestCase):
    """Unit tests for GitHub tools"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_client = Mock()
        self.handler = GitHubToolHandler(self.mock_client)
    
    def test_tool_registry(self):
        """Test that the GitHub tool registry contains expected tools"""
        expected_tools = [
            "github.get_user",
            "github.list_repos",
            "github.list_issues",
            "github.list_pull_requests",
            "github.get_repo"
        ]
        
        for tool in expected_tools:
            self.assertIn(tool, GITHUB_TOOLS, f"Tool {tool} should be in GITHUB_TOOLS")
    
    @patch('api.apps.github.utils.get_github_client_for_user')
    def test_handler_factory(self, mock_get_client):
        """Test that the factory function creates a handler with the client"""
        # Setup mock client and database
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_db = Mock()
        mock_user_id = 123
        
        # Call the factory function
        handler = create_github_handler(mock_user_id, mock_db)
        
        # Check that the handler is a GitHubToolHandler
        self.assertIsInstance(handler, GitHubToolHandler)
        # Check that the handler has the client
        self.assertEqual(handler.client, mock_client)
    
    @patch('api.apps.github.tools.logger')
    def test_execute_get_user(self, mock_logger):
        """Test executing the get_user tool"""
        # Setup mock response
        self.mock_client.get_user.return_value = {"login": "test_user", "id": 12345}
        
        # Call the method
        result = self.handler.execute_tool("github.get_user", {})
        
        # Assert client method was called
        self.mock_client.get_user.assert_called_once()
        
        # Assert the result is the mocked response
        self.assertEqual(result, {"login": "test_user", "id": 12345})
    
    @patch('api.apps.github.tools.logger')
    def test_execute_list_repositories(self, mock_logger):
        """Test executing the list_repos tool"""
        # Setup mock response
        self.mock_client.list_repositories.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        
        # Call the method
        result = self.handler.execute_tool("github.list_repos", {})
        
        # Assert client method was called
        self.mock_client.list_repositories.assert_called_once_with()
        
        # Assert the result is the mocked response
        self.assertEqual(result, {"repositories": [{"name": "repo1"}, {"name": "repo2"}]})
    
    @patch('api.apps.github.tools.logger')
    def test_execute_unknown_tool(self, mock_logger):
        """Test executing an unknown tool"""
        # Call the method with an unknown tool
        with self.assertRaises(ValueError):
            self.handler.execute_tool("github.unknown_tool", {})
        
        # Assert logger was called
        mock_logger.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
