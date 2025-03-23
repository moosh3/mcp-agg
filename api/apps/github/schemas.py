from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class GitHubCredentialBase(BaseModel):
    """Base schema for GitHub credentials"""
    token_type: str = "bearer"
    scope: Optional[str] = None

class GitHubCredentialCreate(GitHubCredentialBase):
    """Schema for creating GitHub credentials"""
    access_token: str

class GitHubCredential(GitHubCredentialBase):
    """Schema for GitHub credential responses"""
    id: int
    user_id: int
    access_token: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class GitHubRepo(BaseModel):
    """Schema for GitHub repository"""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: str
    private: bool

class GitHubIssue(BaseModel):
    """Schema for GitHub issue"""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    html_url: str
    state: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class GitHubPullRequest(BaseModel):
    """Schema for GitHub pull request"""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    html_url: str
    state: str
    created_at: datetime
    updated_at: Optional[datetime] = None
