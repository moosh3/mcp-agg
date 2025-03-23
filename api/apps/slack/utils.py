import logging
from typing import Dict, Optional
from sqlalchemy.orm import Session
from ... import models
from .client import SlackClient

logger = logging.getLogger(__name__)

def get_slack_client_for_user(user_id: int, db: Session) -> SlackClient:
    """Get an authenticated Slack client for the user
    
    Args:
        user_id (int): User ID
        db (Session): Database session
        
    Returns:
        SlackClient: Authenticated Slack client for the user
        
    Raises:
        ValueError: If the user does not have valid Slack credentials
    """
    logger.info(f"Getting Slack client for user {user_id}")
    
    # Get the user's Slack credentials from the database
    slack_credentials = db.query(models.SlackCredentials).filter(
        models.SlackCredentials.user_id == user_id
    ).first()
    
    if not slack_credentials or not slack_credentials.access_token:
        logger.error(f"User {user_id} does not have valid Slack credentials")
        raise ValueError(f"User {user_id} does not have valid Slack credentials")
    
    # Create and return an authenticated Slack client
    return SlackClient(token=slack_credentials.access_token)