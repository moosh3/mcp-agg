import unittest
from unittest.mock import Mock, patch

from api.apps.slack.tools import SlackToolHandler, create_slack_handler, SLACK_TOOLS


class TestSlackTools(unittest.TestCase):
    """Unit tests for Slack tools"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_client = Mock()
        self.handler = SlackToolHandler(self.mock_client)
    
    def test_tool_registry(self):
        """Test that the Slack tool registry contains expected tools"""
        expected_tools = [
            "slack.list_channels",
            "slack.post_message",
            "slack.add_reaction",
            "slack.get_channel_history",
            "slack.get_user_profile"
        ]
        
        for tool in expected_tools:
            self.assertIn(tool, SLACK_TOOLS, f"Tool {tool} should be in SLACK_TOOLS")
    
    @patch('api.apps.slack.utils.get_slack_client_for_user')
    def test_handler_factory(self, mock_get_client):
        """Test that the factory function creates a handler with the client"""
        # Setup mock client and database
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_db = Mock()
        mock_user_id = 123
        
        # Call the factory function
        handler = create_slack_handler(mock_user_id, mock_db)
        
        # Check that the handler is a SlackToolHandler
        self.assertIsInstance(handler, SlackToolHandler)
        # Check that the handler has the client
        self.assertEqual(handler.client, mock_client)
    
    @patch('api.apps.slack.tools.logger')
    def test_execute_list_channels(self, mock_logger):
        """Test executing the list_channels tool"""
        # Setup mock response
        mock_response = {
            "ok": True, 
            "channels": [
                {"id": "C1234", "name": "general"}, 
                {"id": "C5678", "name": "random"}
            ]
        }
        self.mock_client.list_channels.return_value = mock_response
        
        # Call the method
        result = self.handler.execute_tool("slack.list_channels", {"limit": 10})
        
        # Assert client method was called with the limit parameter
        # The actual call might include additional parameters like cursor=None
        assert self.mock_client.list_channels.called
        args, kwargs = self.mock_client.list_channels.call_args
        assert kwargs.get('limit') == 10
        
        # Assert the result contains the expected data structure
        self.assertIn('channels', result)
        self.assertIn('response_metadata', result)
        self.assertEqual(result['channels'], mock_response['channels'])
    
    @patch('api.apps.slack.tools.logger')
    def test_execute_post_message(self, mock_logger):
        """Test executing the post_message tool"""
        # Setup mock response
        mock_response = {
            "ok": True,
            "channel": "C1234",
            "ts": "1234567890.123456"
        }
        self.mock_client.post_message.return_value = mock_response
        
        # Call the method
        result = self.handler.execute_tool("slack.post_message", {
            "channel_id": "C1234",
            "text": "Hello world!"
        })
        
        # Assert client method was called
        self.mock_client.post_message.assert_called_once_with(
            channel_id="C1234",
            text="Hello world!"
        )
        
        # Assert the result contains the expected post_message response structure
        self.assertIn('message', result)
        self.assertIn('ts', result)
        self.assertIn('channel', result)
        self.assertEqual(result['ts'], mock_response['ts'])
        self.assertEqual(result['channel'], mock_response['channel'])
    
    @patch('api.apps.slack.tools.logger')
    def test_execute_unknown_tool(self, mock_logger):
        """Test executing an unknown tool"""
        # Call the method with an unknown tool
        with self.assertRaises(ValueError):
            self.handler.execute_tool("slack.unknown_tool", {})
        
        # Assert logger was called
        mock_logger.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
