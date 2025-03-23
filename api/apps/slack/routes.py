from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from api.database import get_db
from api.dependencies import get_current_active_user
from api.models import User
from .models import SlackCredential
from .schemas import SlackCredentialCreate, SlackCredential as SlackCredentialSchema
from .client import SlackClient

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/apps/slack",
    tags=["slack"],
    responses={404: {"description": "Not found"}},
)


def get_slack_client(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get an authenticated Slack client for the current user.
    
    Args:
        db (Session): Database session
        current_user (User): Current authenticated user
        
    Returns:
        SlackClient: Authenticated Slack client
        
    Raises:
        HTTPException: If Slack credentials are not found
    """
    credentials = db.query(SlackCredential).filter(SlackCredential.user_id == current_user.id).first()
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slack credentials not found. Please connect your Slack account."
        )
    
    return SlackClient(credentials.access_token)


@router.post("/connect", response_model=SlackCredentialSchema)
def connect_slack(credentials: SlackCredentialCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Connect Slack account by providing an OAuth access token.
    
    Args:
        credentials (SlackCredentialCreate): Slack credentials
        db (Session): Database session
        current_user (User): Current authenticated user
        
    Returns:
        SlackCredentialSchema: Saved Slack credentials
    """
    # Check if user already has Slack credentials
    existing_credentials = db.query(SlackCredential).filter(SlackCredential.user_id == current_user.id).first()
    
    if existing_credentials:
        # Update existing credentials
        existing_credentials.access_token = credentials.access_token
        existing_credentials.token_type = credentials.token_type
        existing_credentials.scope = credentials.scope
        existing_credentials.team_id = credentials.team_id
        existing_credentials.team_name = credentials.team_name
        db.commit()
        db.refresh(existing_credentials)
        return existing_credentials
    
    # Create new credentials
    db_credentials = SlackCredential(
        user_id=current_user.id,
        access_token=credentials.access_token,
        token_type=credentials.token_type,
        scope=credentials.scope,
        team_id=credentials.team_id,
        team_name=credentials.team_name
    )
    
    # Add to database
    db.add(db_credentials)
    db.commit()
    db.refresh(db_credentials)
    
    return db_credentials


@router.get("/channels")
def list_channels(slack_client: SlackClient = Depends(get_slack_client)):
    """List channels for the authenticated Slack workspace.
    
    Args:
        slack_client (SlackClient): Authenticated Slack client
        
    Returns:
        Dict[str, Any]: List of channels
    """
    try:
        channels = slack_client.list_channels()
        return {"channels": channels.get("channels", [])}
    except Exception as e:
        logger.error(f"Error listing Slack channels: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching channels: {str(e)}"
        )


@router.post("/channels/{channel_id}/messages")
def post_message(channel_id: str, text: str, slack_client: SlackClient = Depends(get_slack_client)):
    """Post a message to a channel.
    
    Args:
        channel_id (str): Channel ID
        text (str): Message text
        slack_client (SlackClient): Authenticated Slack client
        
    Returns:
        Dict[str, Any]: Message posting result
    """
    try:
        result = slack_client.post_message(channel_id, text)
        return result
    except Exception as e:
        logger.error(f"Error posting Slack message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error posting message: {str(e)}"
        )


@router.post("/channels/{channel_id}/threads/{thread_ts}/replies")
def reply_to_thread(channel_id: str, thread_ts: str, text: str, slack_client: SlackClient = Depends(get_slack_client)):
    """Reply to a message thread.
    
    Args:
        channel_id (str): Channel ID
        thread_ts (str): Thread timestamp
        text (str): Reply text
        slack_client (SlackClient): Authenticated Slack client
        
    Returns:
        Dict[str, Any]: Reply result
    """
    try:
        result = slack_client.reply_to_thread(channel_id, thread_ts, text)
        return result
    except Exception as e:
        logger.error(f"Error replying to Slack thread: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error posting reply: {str(e)}"
        )


@router.get("/channels/{channel_id}/history")
def get_channel_history(channel_id: str, limit: int = 10, slack_client: SlackClient = Depends(get_slack_client)):
    """Get channel message history.
    
    Args:
        channel_id (str): Channel ID
        limit (int, optional): Number of messages. Defaults to 10.
        slack_client (SlackClient): Authenticated Slack client
        
    Returns:
        Dict[str, Any]: Channel history
    """
    try:
        history = slack_client.get_channel_history(channel_id, limit)
        return history
    except Exception as e:
        logger.error(f"Error getting Slack channel history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching channel history: {str(e)}"
        )


@router.get("/channels/{channel_id}/threads/{thread_ts}/replies")
def get_thread_replies(channel_id: str, thread_ts: str, slack_client: SlackClient = Depends(get_slack_client)):
    """Get replies in a thread.
    
    Args:
        channel_id (str): Channel ID
        thread_ts (str): Thread timestamp
        slack_client (SlackClient): Authenticated Slack client
        
    Returns:
        Dict[str, Any]: Thread replies
    """
    try:
        replies = slack_client.get_thread_replies(channel_id, thread_ts)
        return replies
    except Exception as e:
        logger.error(f"Error getting Slack thread replies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching thread replies: {str(e)}"
        )


@router.get("/users")
def list_users(slack_client: SlackClient = Depends(get_slack_client)):
    """List users in the Slack workspace.
    
    Args:
        slack_client (SlackClient): Authenticated Slack client
        
    Returns:
        Dict[str, Any]: List of users
    """
    try:
        users = slack_client.get_users()
        return {"users": users.get("members", [])}
    except Exception as e:
        logger.error(f"Error listing Slack users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )


@router.get("/users/{user_id}")
def get_user_profile(user_id: str, slack_client: SlackClient = Depends(get_slack_client)):
    """Get user profile.
    
    Args:
        user_id (str): User ID
        slack_client (SlackClient): Authenticated Slack client
        
    Returns:
        Dict[str, Any]: User profile
    """
    try:
        user = slack_client.get_user_profile(user_id)
        return user
    except Exception as e:
        logger.error(f"Error getting Slack user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user profile: {str(e)}"
        )
