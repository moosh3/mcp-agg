import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.usefixtures("client", "test_user", "github_credentials", "slack_credentials")
class TestToolEndpoints:
    """Integration tests for tool endpoints"""    
    
    @patch("api.apps.github.utils.get_github_client_for_user")
    def test_execute_github_tool(self, mock_get_client, client, test_user):
        """Test executing a GitHub tool through the API endpoint"""
        # Setup mock GitHub client
        mock_client = MagicMock()
        mock_client.list_repositories.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_client.return_value = mock_client
        
        # Execute a GitHub tool
        response = client.post(
            "/api/v1/execute/",
            json={
                "tool": "github.list_repos",
                "parameters": {}
            }
        )
        
        # Assert response is successful
        assert response.status_code == 200
        # Assert response contains expected data
        assert "success" in response.json()
        assert "result" in response.json()
        # Assert client was called correctly
        mock_client.list_repositories.assert_called_once()
    
    @patch("api.apps.slack.utils.get_slack_client_for_user")
    def test_execute_slack_tool(self, mock_get_client, client, test_user):
        """Test executing a Slack tool through the API endpoint"""
        # Setup mock Slack client
        mock_client = MagicMock()
        mock_client.list_channels.return_value = {
            "ok": True,
            "channels": [{"id": "C1234", "name": "general"}]
        }
        mock_get_client.return_value = mock_client
        
        # Execute a Slack tool
        response = client.post(
            "/api/v1/execute/",
            json={
                "tool": "slack.list_channels",
                "parameters": {"limit": 10}
            }
        )
        
        # Assert response is successful
        assert response.status_code == 200
        # Assert response contains expected data
        assert "success" in response.json()
        assert "result" in response.json()
        # Assert client was called correctly
        # The actual call includes a cursor=None parameter which is fine
        assert mock_client.list_channels.called
        args, kwargs = mock_client.list_channels.call_args
        assert kwargs.get('limit') == 10
    
    def test_unknown_tool(self, client):
        """Test attempting to execute an unknown tool"""
        response = client.post(
            "/api/v1/execute/",
            json={
                "tool": "unknown.tool",
                "parameters": {}
            }
        )
        
        # Assert response indicates an error (400 for unknown app, 404 for unknown tool in known app)
        assert response.status_code in [400, 404]
    
    def test_generate_mcp_url(self, client, test_user, github_credentials, slack_credentials):
        """Test generating an MCP URL for the authenticated user"""
        
        # Call the MCP URL endpoint
        response = client.get("/api/v1/mcp-url/")
        
        # Assert response is successful
        assert response.status_code == 200
        
        # Assert response contains expected fields
        data = response.json()
        assert "url" in data
        assert "expires_at" in data
        assert "description" in data
        
        # URL should contain a token
        assert "token=" in data["url"]
        
        # Description should mention github and slack apps
        assert "github" in data["description"]
        assert "slack" in data["description"]
