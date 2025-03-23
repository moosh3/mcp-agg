import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .client import GitHubClient

logger = logging.getLogger(__name__)


def format_tool_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format the result of a GitHub tool execution for MCP response
    
    Args:
        result (Dict[str, Any]): Raw result from GitHub API
        
    Returns:
        Dict[str, Any]: Formatted result suitable for MCP response
    """
    # Ensure datetime objects are converted to strings
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict) or isinstance(value, list):
                result[key] = format_tool_result(value)
    elif isinstance(result, list):
        result = [format_tool_result(item) if isinstance(item, (dict, list)) else item for item in result]
    
    return result


def validate_github_credentials(access_token: str) -> bool:
    """Validate GitHub credentials by making a simple API call
    
    Args:
        access_token (str): GitHub access token to validate
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    try:
        client = GitHubClient(access_token)
        client.get_user()  # Try to get user info
        return True
    except Exception as e:
        logger.error(f"GitHub credential validation failed: {e}")
        return False


def get_github_client_for_user(user_id: int, db) -> GitHubClient:
    """Get an authenticated GitHub client for a specific user
    
    Args:
        user_id (int): User ID
        db: Database session
        
    Returns:
        GitHubClient: Authenticated GitHub client
        
    Raises:
        HTTPException: If GitHub credentials are not found
    """
    from fastapi import HTTPException, status
    from sqlalchemy.orm import Session
    from .models import GitHubCredential
    
    # Get credentials from the database
    credentials = db.query(GitHubCredential).filter(
        GitHubCredential.user_id == user_id
    ).first()
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GitHub credentials not found for this user. Please connect to GitHub first."
        )
    
    # Create and return a GitHub client with the user's access token
    return GitHubClient(credentials.access_token)
