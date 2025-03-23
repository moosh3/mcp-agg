from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class SlackCredentialBase(BaseModel):
    """Base schema for Slack credentials"""
    token_type: str = "bearer"
    scope: Optional[str] = None
    team_id: Optional[str] = None
    team_name: Optional[str] = None

class SlackCredentialCreate(SlackCredentialBase):
    """Schema for creating Slack credentials"""
    access_token: str

class SlackCredential(SlackCredentialBase):
    """Schema for Slack credential responses"""
    id: int
    user_id: int
    access_token: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SlackChannel(BaseModel):
    """Schema for Slack channel"""
    id: str
    name: str
    is_private: bool
    num_members: Optional[int] = None

class SlackMessage(BaseModel):
    """Schema for Slack message"""
    ts: str
    text: str
    user: str
    channel: str
    thread_ts: Optional[str] = None

class SlackUser(BaseModel):
    """Schema for Slack user"""
    id: str
    name: str
    real_name: Optional[str] = None
    is_bot: bool
    profile: Dict[str, Any]
