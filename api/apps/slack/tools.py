import logging
from typing import Dict, List, Any, Optional
from .client import SlackClient

logger = logging.getLogger(__name__)

# Define Slack tools with their parameters
SLACK_TOOLS = {
    "slack.list_channels": {
        "name": "slack.list_channels",
        "description": "List public channels in the workspace",
        "parameters": {
            "limit": {
                "type": "number",
                "description": "Maximum number of channels to return (default: 100, max: 200)",
                "optional": True
            },
            "cursor": {
                "type": "string",
                "description": "Pagination cursor for next page",
                "optional": True
            }
        }
    },
    "slack.post_message": {
        "name": "slack.post_message",
        "description": "Post a new message to a Slack channel",
        "parameters": {
            "channel_id": {
                "type": "string",
                "description": "The ID of the channel to post to"
            },
            "text": {
                "type": "string",
                "description": "The message text to post"
            }
        }
    },
    "slack.reply_to_thread": {
        "name": "slack.reply_to_thread",
        "description": "Reply to a specific message thread",
        "parameters": {
            "channel_id": {
                "type": "string",
                "description": "The channel containing the thread"
            },
            "thread_ts": {
                "type": "string",
                "description": "Timestamp of the parent message"
            },
            "text": {
                "type": "string",
                "description": "The reply text"
            }
        }
    },
    "slack.add_reaction": {
        "name": "slack.add_reaction",
        "description": "Add an emoji reaction to a message",
        "parameters": {
            "channel_id": {
                "type": "string",
                "description": "The channel containing the message"
            },
            "timestamp": {
                "type": "string",
                "description": "Message timestamp to react to"
            },
            "reaction": {
                "type": "string",
                "description": "Emoji name without colons"
            }
        }
    },
    "slack.get_channel_history": {
        "name": "slack.get_channel_history",
        "description": "Get recent messages from a channel",
        "parameters": {
            "channel_id": {
                "type": "string",
                "description": "The channel ID"
            },
            "limit": {
                "type": "number",
                "description": "Number of messages to retrieve (default: 10)",
                "optional": True
            }
        }
    },
    "slack.get_thread_replies": {
        "name": "slack.get_thread_replies",
        "description": "Get all replies in a message thread",
        "parameters": {
            "channel_id": {
                "type": "string",
                "description": "The channel containing the thread"
            },
            "thread_ts": {
                "type": "string",
                "description": "Timestamp of the parent message"
            }
        }
    },
    "slack.get_users": {
        "name": "slack.get_users",
        "description": "Get list of workspace users with basic profile information",
        "parameters": {
            "cursor": {
                "type": "string",
                "description": "Pagination cursor for next page",
                "optional": True
            },
            "limit": {
                "type": "number",
                "description": "Maximum users to return (default: 100, max: 200)",
                "optional": True
            }
        }
    },
    "slack.get_user_profile": {
        "name": "slack.get_user_profile",
        "description": "Get detailed profile information for a specific user",
        "parameters": {
            "user_id": {
                "type": "string",
                "description": "The user's ID"
            }
        }
    }
}


# Factory function to create a Slack tool handler for a user
def create_slack_handler(user_id: int, db):
    """Factory function to create a Slack tool handler for a user
    
    Args:
        user_id (int): User ID
        db: Database session
        
    Returns:
        SlackToolHandler: Handler for Slack tools
    """
    from .utils import get_slack_client_for_user
    client = get_slack_client_for_user(user_id, db)
    return SlackToolHandler(client)


class SlackToolHandler:
    """Handler for executing Slack tools via MCP"""
    
    def __init__(self, slack_client: SlackClient):
        """Initialize with Slack client
        
        Args:
            slack_client (SlackClient): Authenticated Slack client
        """
        self.client = slack_client
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get all Slack tool definitions
        
        Returns:
            List[Dict[str, Any]]: List of tool definitions
        """
        return list(SLACK_TOOLS.values())
    
    def list_channels(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """List public channels in the workspace
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including limit and cursor
            
        Returns:
            Dict[str, Any]: Channels and response metadata
        """
        limit = parameters.get("limit", 100)
        cursor = parameters.get("cursor", None)
        response = self.client.list_channels(limit=limit, cursor=cursor)
        return {
            "channels": response.get("channels", []),
            "response_metadata": response.get("response_metadata", {})
        }
    
    def post_message(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Post a new message to a Slack channel
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including channel_id and text
            
        Returns:
            Dict[str, Any]: Message info including timestamp and channel
        """
        channel_id = parameters["channel_id"]
        text = parameters["text"]
        response = self.client.post_message(channel_id=channel_id, text=text)
        return {
            "message": "Message posted successfully",
            "ts": response.get("ts"),
            "channel": response.get("channel")
        }
    
    def reply_to_thread(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Reply to a specific message thread
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including channel_id, thread_ts, and text
            
        Returns:
            Dict[str, Any]: Reply info including timestamp and channel
        """
        channel_id = parameters["channel_id"]
        thread_ts = parameters["thread_ts"]
        text = parameters["text"]
        response = self.client.reply_to_thread(channel_id=channel_id, thread_ts=thread_ts, text=text)
        return {
            "message": "Reply posted successfully",
            "ts": response.get("ts"),
            "channel": response.get("channel")
        }
    
    def add_reaction(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Add an emoji reaction to a message
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including channel_id, timestamp, and reaction
            
        Returns:
            Dict[str, Any]: Success message
        """
        channel_id = parameters["channel_id"]
        timestamp = parameters["timestamp"]
        reaction = parameters["reaction"]
        response = self.client.add_reaction(channel_id=channel_id, timestamp=timestamp, reaction=reaction)
        return {
            "message": "Reaction added successfully"
        }
    
    def get_channel_history(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get recent messages from a channel
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including channel_id and limit
            
        Returns:
            Dict[str, Any]: Messages and pagination info
        """
        channel_id = parameters["channel_id"]
        limit = parameters.get("limit", 10)
        response = self.client.get_channel_history(channel_id=channel_id, limit=limit)
        return {
            "messages": response.get("messages", []),
            "has_more": response.get("has_more", False)
        }
    
    def get_thread_replies(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get all replies in a message thread
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including channel_id and thread_ts
            
        Returns:
            Dict[str, Any]: Thread messages
        """
        channel_id = parameters["channel_id"]
        thread_ts = parameters["thread_ts"]
        response = self.client.get_thread_replies(channel_id=channel_id, thread_ts=thread_ts)
        return {
            "messages": response.get("messages", [])
        }
    
    def get_users(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get list of workspace users with basic profile information
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including cursor and limit
            
        Returns:
            Dict[str, Any]: Users and response metadata
        """
        cursor = parameters.get("cursor", None)
        limit = parameters.get("limit", 100)
        response = self.client.get_users(cursor=cursor, limit=limit)
        return {
            "members": response.get("members", []),
            "response_metadata": response.get("response_metadata", {})
        }
    
    def get_user_profile(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed profile information for a specific user
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including user_id
            
        Returns:
            Dict[str, Any]: User profile information
        """
        user_id = parameters["user_id"]
        response = self.client.get_user_profile(user_id=user_id)
        return {
            "user": response.get("user", {})
        }
        
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a Slack tool with the given parameters
        
        Args:
            tool_name (str): Name of the tool to execute
            parameters (Dict[str, Any]): Tool parameters
            
        Returns:
            Dict[str, Any]: Result of the tool execution
            
        Raises:
            ValueError: If the tool name is invalid
        """
        logger.info(f"Executing Slack tool: {tool_name} with parameters: {parameters}")
        
        if tool_name not in SLACK_TOOLS:
            logger.error(f"Unknown Slack tool: {tool_name}")
            raise ValueError(f"Unknown Slack tool: {tool_name}")
        
        # Get the method name by removing the 'slack.' prefix
        method_name = tool_name.replace('slack.', '')
        
        try:
            # Get the method dynamically and call it with the parameters
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                return method(parameters)
            else:
                logger.error(f"Unimplemented Slack tool: {tool_name}")
                raise ValueError(f"Unimplemented Slack tool: {tool_name}")
        except Exception as e:
            logger.error(f"Error executing Slack tool {tool_name}: {str(e)}")
            raise