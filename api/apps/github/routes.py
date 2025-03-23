from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from api.database import get_db
from api.dependencies import get_current_active_user
from api.models import User
from .models import GitHubCredential
from .schemas import GitHubCredentialCreate, GitHubCredential as GitHubCredentialSchema
from .client import GitHubClient

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/apps/github",
    tags=["github"],
    responses={404: {"description": "Not found"}},
)


def get_github_client(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get an authenticated GitHub client for the current user.
    
    Args:
        db (Session): Database session
        current_user (User): Current authenticated user
        
    Returns:
        GitHubClient: Authenticated GitHub client
        
    Raises:
        HTTPException: If GitHub credentials are not found
    """
    credentials = db.query(GitHubCredential).filter(GitHubCredential.user_id == current_user.id).first()
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GitHub credentials not found. Please connect your GitHub account."
        )
    
    return GitHubClient(credentials.access_token)


@router.post("/connect", response_model=GitHubCredentialSchema)
def connect_github(credentials: GitHubCredentialCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Connect GitHub account by providing an OAuth access token.
    
    Args:
        credentials (GitHubCredentialCreate): GitHub credentials
        db (Session): Database session
        current_user (User): Current authenticated user
        
    Returns:
        GitHubCredentialSchema: Saved GitHub credentials
    """
    # Check if user already has GitHub credentials
    existing_credentials = db.query(GitHubCredential).filter(GitHubCredential.user_id == current_user.id).first()
    
    if existing_credentials:
        # Update existing credentials
        existing_credentials.access_token = credentials.access_token
        existing_credentials.token_type = credentials.token_type
        existing_credentials.scope = credentials.scope
        db.commit()
        db.refresh(existing_credentials)
        return existing_credentials
    
    # Create new credentials
    db_credentials = GitHubCredential(
        user_id=current_user.id,
        access_token=credentials.access_token,
        token_type=credentials.token_type,
        scope=credentials.scope
    )
    
    # Add to database
    db.add(db_credentials)
    db.commit()
    db.refresh(db_credentials)
    
    return db_credentials


@router.get("/repositories")
def list_repositories(github_client: GitHubClient = Depends(get_github_client)):
    """List repositories for the authenticated GitHub user.
    
    Args:
        github_client (GitHubClient): Authenticated GitHub client
        
    Returns:
        Dict[str, Any]: List of repositories
    """
    try:
        repos = github_client.list_repositories()
        return {"repositories": repos}
    except Exception as e:
        logger.error(f"Error listing GitHub repositories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching repositories: {str(e)}"
        )


@router.get("/user")
def get_user(github_client: GitHubClient = Depends(get_github_client)):
    """Get authenticated GitHub user information.
    
    Args:
        github_client (GitHubClient): Authenticated GitHub client
        
    Returns:
        Dict[str, Any]: User information
    """
    try:
        user = github_client.get_user()
        return user
    except Exception as e:
        logger.error(f"Error getting GitHub user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user information: {str(e)}"
        )


@router.get("/repositories/{owner}/{repo}/issues")
def list_issues(owner: str, repo: str, github_client: GitHubClient = Depends(get_github_client)):
    """List issues for a GitHub repository.
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        github_client (GitHubClient): Authenticated GitHub client
        
    Returns:
        Dict[str, Any]: List of issues
    """
    try:
        issues = github_client.list_issues(owner, repo)
        return {"issues": issues}
    except Exception as e:
        logger.error(f"Error listing GitHub issues: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching issues: {str(e)}"
        )


@router.post("/repositories/{owner}/{repo}/issues")
def create_issue(owner: str, repo: str, title: str, body: str = None, github_client: GitHubClient = Depends(get_github_client)):
    """Create a new issue in a GitHub repository.
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        title (str): Issue title
        body (str, optional): Issue body. Defaults to None.
        github_client (GitHubClient): Authenticated GitHub client
        
    Returns:
        Dict[str, Any]: Created issue information
    """
    try:
        issue = github_client.create_issue(owner, repo, title, body)
        return issue
    except Exception as e:
        logger.error(f"Error creating GitHub issue: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating issue: {str(e)}"
        )
