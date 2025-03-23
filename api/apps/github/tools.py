from typing import Dict, List, Any, Optional
import logging
from .client import GitHubClient

logger = logging.getLogger(__name__)

# Dictionary of GitHub tool definitions to be exposed via MCP
GITHUB_TOOLS = {
    "github.get_user": {
        "name": "github.get_user",
        "description": "Get authenticated GitHub user information",
        "parameters": {}
    },
    "github.list_repos": {
        "name": "github.list_repos",
        "description": "List GitHub repositories for the authenticated user",
        "parameters": {}
    },
    "github.get_repo": {
        "name": "github.get_repo",
        "description": "Get information about a specific GitHub repository",
        "parameters": {
            "owner": {
                "type": "string",
                "description": "Repository owner username"
            },
            "repo": {
                "type": "string",
                "description": "Repository name"
            }
        }
    },
    "github.list_issues": {
        "name": "github.list_issues",
        "description": "List issues for a GitHub repository",
        "parameters": {
            "owner": {
                "type": "string",
                "description": "Repository owner username"
            },
            "repo": {
                "type": "string",
                "description": "Repository name"
            }
        }
    },
    "github.create_issue": {
        "name": "github.create_issue",
        "description": "Create a new issue in a GitHub repository",
        "parameters": {
            "owner": {
                "type": "string",
                "description": "Repository owner username"
            },
            "repo": {
                "type": "string",
                "description": "Repository name"
            },
            "title": {
                "type": "string",
                "description": "Issue title"
            },
            "body": {
                "type": "string",
                "description": "Issue body (description)",
                "optional": True
            }
        }
    },
    "github.list_pull_requests": {
        "name": "github.list_pull_requests",
        "description": "List pull requests for a GitHub repository",
        "parameters": {
            "owner": {
                "type": "string",
                "description": "Repository owner username"
            },
            "repo": {
                "type": "string",
                "description": "Repository name"
            }
        }
    },
    "github.create_pull_request": {
        "name": "github.create_pull_request",
        "description": "Create a new pull request in a GitHub repository",
        "parameters": {
            "owner": {
                "type": "string",
                "description": "Repository owner username"
            },
            "repo": {
                "type": "string",
                "description": "Repository name"
            },
            "title": {
                "type": "string",
                "description": "Pull request title"
            },
            "head": {
                "type": "string",
                "description": "The name of the branch where changes are implemented"
            },
            "base": {
                "type": "string",
                "description": "The name of the branch to pull changes into"
            },
            "body": {
                "type": "string",
                "description": "Pull request body (description)",
                "optional": True
            }
        }
    }
}


# Factory function to create a GitHub tool handler for a user
def create_github_handler(user_id: int, db):
    """Factory function to create a GitHub tool handler for a user
    
    Args:
        user_id (int): User ID
        db: Database session
        
    Returns:
        GitHubToolHandler: Handler for GitHub tools
    """
    from .utils import get_github_client_for_user
    client = get_github_client_for_user(user_id, db)
    return GitHubToolHandler(client)


class GitHubToolHandler:
    """Handler for executing GitHub tools via MCP"""
    
    def __init__(self, github_client: GitHubClient):
        """Initialize with GitHub client
        
        Args:
            github_client (GitHubClient): Authenticated GitHub client
        """
        self.client = github_client
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get all GitHub tool definitions
        
        Returns:
            List[Dict[str, Any]]: List of tool definitions
        """
        return list(GITHUB_TOOLS.values())
    
    def get_user(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get authenticated GitHub user information
        
        Args:
            parameters (Dict[str, Any]): Tool parameters (none required)
            
        Returns:
            Dict[str, Any]: User information
        """
        return self.client.get_user()
    
    def list_repos(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """List GitHub repositories for the authenticated user
        
        Args:
            parameters (Dict[str, Any]): Tool parameters (none required)
            
        Returns:
            Dict[str, Any]: Repository list
        """
        return {"repositories": self.client.list_repositories()}
    
    def get_repo(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get information about a specific GitHub repository
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including owner and repo
            
        Returns:
            Dict[str, Any]: Repository information
            
        Raises:
            ValueError: If required parameters are missing
        """
        owner = parameters.get("owner")
        repo = parameters.get("repo")
        if not owner or not repo:
            raise ValueError("owner and repo parameters are required")
        
        return self.client.get_repository(owner, repo)
    
    def list_issues(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """List issues for a GitHub repository
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including owner and repo
            
        Returns:
            Dict[str, Any]: Issues list
            
        Raises:
            ValueError: If required parameters are missing
        """
        owner = parameters.get("owner")
        repo = parameters.get("repo")
        if not owner or not repo:
            raise ValueError("owner and repo parameters are required")
        
        return {"issues": self.client.list_issues(owner, repo)}
    
    def create_issue(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new issue in a GitHub repository
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including owner, repo, title, and optional body
            
        Returns:
            Dict[str, Any]: Created issue information
            
        Raises:
            ValueError: If required parameters are missing
        """
        owner = parameters.get("owner")
        repo = parameters.get("repo")
        title = parameters.get("title")
        body = parameters.get("body")
        
        if not owner or not repo or not title:
            raise ValueError("owner, repo, and title parameters are required")
        
        return self.client.create_issue(owner, repo, title, body)
    
    def list_pull_requests(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """List pull requests for a GitHub repository
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including owner and repo
            
        Returns:
            Dict[str, Any]: Pull requests list
            
        Raises:
            ValueError: If required parameters are missing
        """
        owner = parameters.get("owner")
        repo = parameters.get("repo")
        if not owner or not repo:
            raise ValueError("owner and repo parameters are required")
        
        return {"pull_requests": self.client.list_pull_requests(owner, repo)}
    
    def create_pull_request(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new pull request in a GitHub repository
        
        Args:
            parameters (Dict[str, Any]): Tool parameters including owner, repo, title, head, base, and optional body
            
        Returns:
            Dict[str, Any]: Created pull request information
            
        Raises:
            ValueError: If required parameters are missing
        """
        owner = parameters.get("owner")
        repo = parameters.get("repo")
        title = parameters.get("title")
        head = parameters.get("head")
        base = parameters.get("base")
        body = parameters.get("body")
        
        if not owner or not repo or not title or not head or not base:
            raise ValueError("owner, repo, title, head, and base parameters are required")
        
        return self.client.create_pull_request(owner, repo, title, head, base, body)
        
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a GitHub tool with the given parameters
        
        Args:
            tool_name (str): Name of the tool to execute
            parameters (Dict[str, Any]): Tool parameters
            
        Returns:
            Dict[str, Any]: Result of the tool execution
            
        Raises:
            ValueError: If the tool name is invalid
        """
        logger.info(f"Executing GitHub tool: {tool_name} with parameters: {parameters}")
        
        if tool_name not in GITHUB_TOOLS:
            logger.error(f"Unknown GitHub tool: {tool_name}")
            raise ValueError(f"Unknown GitHub tool: {tool_name}")
        
        # Get the method name by removing the 'github.' prefix
        method_name = tool_name.replace('github.', '')
        
        try:
            # Get the method dynamically and call it with the parameters
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                return method(parameters)
            else:
                logger.error(f"Unimplemented GitHub tool: {tool_name}")
                raise ValueError(f"Unimplemented GitHub tool: {tool_name}")
        except Exception as e:
            logger.error(f"Error executing GitHub tool {tool_name}: {str(e)}")
            return {"error": str(e)}
