import requests
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class GitHubClient:
    """Client for interacting with GitHub API"""
    BASE_URL = "https://api.github.com"
    
    def __init__(self, access_token: str):
        """Initialize GitHub client with access token
        
        Args:
            access_token (str): GitHub OAuth access token
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the GitHub API
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint path
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Dict[str, Any]: JSON response from API
            
        Raises:
            Exception: If the request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API request failed: {e}")
            raise
    
    def get_user(self) -> Dict[str, Any]:
        """Get authenticated user information
        
        Returns:
            Dict[str, Any]: User information
        """
        return self._make_request("GET", "/user")
    
    def list_repositories(self) -> List[Dict[str, Any]]:
        """List repositories for the authenticated user
        
        Returns:
            List[Dict[str, Any]]: List of repositories
        """
        return self._make_request("GET", "/user/repos")
    
    def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            
        Returns:
            Dict[str, Any]: Repository information
        """
        return self._make_request("GET", f"/repos/{owner}/{repo}")
    
    def list_issues(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """List issues for a repository
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            
        Returns:
            List[Dict[str, Any]]: List of issues
        """
        return self._make_request("GET", f"/repos/{owner}/{repo}/issues")
    
    def create_issue(self, owner: str, repo: str, title: str, body: Optional[str] = None) -> Dict[str, Any]:
        """Create a new issue
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            title (str): Issue title
            body (Optional[str], optional): Issue body. Defaults to None.
            
        Returns:
            Dict[str, Any]: Created issue information
        """
        data = {"title": title}
        if body:
            data["body"] = body
        
        return self._make_request(
            "POST",
            f"/repos/{owner}/{repo}/issues",
            json=data
        )
    
    def list_pull_requests(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """List pull requests for a repository
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            
        Returns:
            List[Dict[str, Any]]: List of pull requests
        """
        return self._make_request("GET", f"/repos/{owner}/{repo}/pulls")
    
    def create_pull_request(self, owner: str, repo: str, title: str, head: str, base: str, body: Optional[str] = None) -> Dict[str, Any]:
        """Create a new pull request
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            title (str): Pull request title
            head (str): The name of the branch where your changes are implemented
            base (str): The name of the branch you want the changes pulled into
            body (Optional[str], optional): Pull request body. Defaults to None.
            
        Returns:
            Dict[str, Any]: Created pull request information
        """
        data = {
            "title": title,
            "head": head,
            "base": base
        }
        if body:
            data["body"] = body
        
        return self._make_request(
            "POST",
            f"/repos/{owner}/{repo}/pulls",
            json=data
        )
