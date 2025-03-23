import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# Add the project root to the Python path to allow importing modules without installing the package
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from api.apps.github.client import GitHubClient


class TestGitHubClient(unittest.TestCase):
    """Unit tests for GitHubClient class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.access_token = "test_token"
        self.client = GitHubClient(access_token=self.access_token)
    
    def test_initialization(self):
        """Test client initialization sets the correct properties"""
        self.assertEqual(self.client.access_token, self.access_token)
        self.assertEqual(self.client.headers["Authorization"], f"Bearer {self.access_token}")
    
    @patch('api.apps.github.client.requests.request')
    def test_get_user(self, mock_request):
        """Test get_user method makes correct API call"""
        # Setup mock response
        mock_response = Mock()
        mock_response.content = True
        mock_response.json.return_value = {"login": "test_user", "id": 12345}
        mock_request.return_value = mock_response
        
        # Call the method
        result = self.client.get_user()
        
        # Assert requests.request was called with correct args
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.github.com/user",
            headers=self.client.headers
        )
        
        # Assert the result is the mocked response
        self.assertEqual(result, {"login": "test_user", "id": 12345})
    
    @patch('api.apps.github.client.requests.request')
    def test_list_repositories(self, mock_request):
        """Test list_repositories method makes correct API call"""
        # Setup mock response
        mock_response = Mock()
        mock_response.content = True
        mock_response.json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        mock_request.return_value = mock_response
        
        # Call the method
        result = self.client.list_repositories()
        
        # Assert requests.request was called with correct args
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.github.com/user/repos",
            headers=self.client.headers
        )
        
        # Assert the result is the mocked response
        self.assertEqual(result, [{"name": "repo1"}, {"name": "repo2"}])


if __name__ == "__main__":
    unittest.main()
