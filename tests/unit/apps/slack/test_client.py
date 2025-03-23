import unittest
from unittest.mock import Mock, patch

from api.apps.slack.client import SlackClient


class TestSlackClient(unittest.TestCase):
    """Unit tests for SlackClient class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.token = "xoxp-test-token"
        self.client = SlackClient(token=self.token)
    
    def test_initialization(self):
        """Test client initialization sets the correct properties"""
        self.assertEqual(self.client.token, self.token)
        self.assertEqual(self.client.headers["Authorization"], f"Bearer {self.token}")
    
    @patch('api.apps.slack.client.requests.get')
    def test_list_channels(self, mock_get):
        """Test list_channels method makes correct API call"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "ok": True, 
            "channels": [
                {"id": "C1234", "name": "general"}, 
                {"id": "C5678", "name": "random"}
            ]
        }
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.list_channels(limit=10)
        
        # Assert requests.get was called with correct args
        mock_get.assert_called_once_with(
            "https://slack.com/api/conversations.list",
            headers=self.client.headers,
            params={"limit": 10}
        )
        
        # Assert the result is the mocked response
        self.assertEqual(result, {
            "ok": True, 
            "channels": [
                {"id": "C1234", "name": "general"}, 
                {"id": "C5678", "name": "random"}
            ]
        })
    
    @patch('api.apps.slack.client.requests.post')
    def test_post_message(self, mock_post):
        """Test post_message method makes correct API call"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "ok": True,
            "channel": "C1234",
            "ts": "1234567890.123456"
        }
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.client.post_message(
            channel_id="C1234",
            text="Hello world!"
        )
        
        # Assert requests.post was called with correct args
        mock_post.assert_called_once_with(
            "https://slack.com/api/chat.postMessage",
            headers=self.client.headers,
            json={
                "channel": "C1234",
                "text": "Hello world!"
            }
        )
        
        # Assert the result is the mocked response
        self.assertEqual(result, {
            "ok": True,
            "channel": "C1234",
            "ts": "1234567890.123456"
        })
    
    @patch('api.apps.slack.client.requests.post')
    def test_add_reaction(self, mock_post):
        """Test add_reaction method makes correct API call"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.client.add_reaction(
            channel_id="C1234",
            timestamp="1234567890.123456",
            reaction="thumbsup"
        )
        
        # Assert requests.post was called with correct args
        mock_post.assert_called_once_with(
            "https://slack.com/api/reactions.add",
            headers=self.client.headers,
            json={
                "channel": "C1234",
                "timestamp": "1234567890.123456",
                "name": "thumbsup"
            }
        )
        
        # Assert the result is the mocked response
        self.assertEqual(result, {"ok": True})


if __name__ == "__main__":
    unittest.main()
