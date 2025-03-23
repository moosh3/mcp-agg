import logging
import requests
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class SlackClient:
    """Client for interacting with Slack API"""
    
    BASE_URL = "https://slack.com/api"
    
    def __init__(self, token: str):
        """Initialize with Slack API token
        
        Args:
            token (str): Slack API token
        """
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, json_data: Dict = None) -> Dict[str, Any]:
        """Make a request to the Slack API
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            params (Dict, optional): Query parameters
            json_data (Dict, optional): JSON data for POST requests
            
        Returns:
            Dict[str, Any]: Response data
            
        Raises:
            Exception: If the request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            logger.info(f"Making {method} request to {url}")
            
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=json_data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            data = response.json()
            
            if not data.get("ok", False):
                error_message = data.get("error", "Unknown error")
                logger.error(f"Slack API error: {error_message}")
                raise Exception(f"Slack API error: {error_message}")
            
            return data
            
        except Exception as e:
            logger.error(f"Error making request to Slack API: {str(e)}")
            raise
    
    def list_channels(self, limit: int = 100, cursor: str = None) -> Dict[str, Any]:
        """List public channels in the workspace
        
        Args:
            limit (int, optional): Maximum number of channels. Defaults to 100.
            cursor (str, optional): Pagination cursor. Defaults to None.
            
        Returns:
            Dict[str, Any]: List of channels
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
            
        return self._make_request("GET", "conversations.list", params=params)
    
    def post_message(self, channel_id: str, text: str) -> Dict[str, Any]:
        """Post a message to a channel
        
        Args:
            channel_id (str): Channel ID
            text (str): Message text
            
        Returns:
            Dict[str, Any]: Message posting result
        """
        json_data = {
            "channel": channel_id,
            "text": text
        }
        
        return self._make_request("POST", "chat.postMessage", json_data=json_data)
    
    def reply_to_thread(self, channel_id: str, thread_ts: str, text: str) -> Dict[str, Any]:
        """Reply to a thread
        
        Args:
            channel_id (str): Channel ID
            thread_ts (str): Thread timestamp
            text (str): Reply text
            
        Returns:
            Dict[str, Any]: Reply result
        """
        json_data = {
            "channel": channel_id,
            "thread_ts": thread_ts,
            "text": text
        }
        
        return self._make_request("POST", "chat.postMessage", json_data=json_data)
    
    def add_reaction(self, channel_id: str, timestamp: str, reaction: str) -> Dict[str, Any]:
        """Add a reaction to a message
        
        Args:
            channel_id (str): Channel ID
            timestamp (str): Message timestamp
            reaction (str): Emoji name without colons
            
        Returns:
            Dict[str, Any]: Reaction result
        """
        json_data = {
            "channel": channel_id,
            "timestamp": timestamp,
            "name": reaction
        }
        
        return self._make_request("POST", "reactions.add", json_data=json_data)
    
    def get_channel_history(self, channel_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get channel message history
        
        Args:
            channel_id (str): Channel ID
            limit (int, optional): Number of messages. Defaults to 10.
            
        Returns:
            Dict[str, Any]: Channel history
        """
        params = {
            "channel": channel_id,
            "limit": limit
        }
        
        return self._make_request("GET", "conversations.history", params=params)
    
    def get_thread_replies(self, channel_id: str, thread_ts: str) -> Dict[str, Any]:
        """Get replies in a thread
        
        Args:
            channel_id (str): Channel ID
            thread_ts (str): Thread timestamp
            
        Returns:
            Dict[str, Any]: Thread replies
        """
        params = {
            "channel": channel_id,
            "ts": thread_ts
        }
        
        return self._make_request("GET", "conversations.replies", params=params)
    
    def get_users(self, cursor: str = None, limit: int = 100) -> Dict[str, Any]:
        """Get workspace users
        
        Args:
            cursor (str, optional): Pagination cursor. Defaults to None.
            limit (int, optional): Maximum number of users. Defaults to 100.
            
        Returns:
            Dict[str, Any]: List of users
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
            
        return self._make_request("GET", "users.list", params=params)
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile
        
        Args:
            user_id (str): User ID
            
        Returns:
            Dict[str, Any]: User profile
        """
        params = {"user": user_id}
        
        return self._make_request("GET", "users.info", params=params)