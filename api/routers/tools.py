from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api import schemas, models, database
from api.dependencies import get_current_active_user
from api.apps.github.tools import GITHUB_TOOLS, create_github_handler
from api.apps.slack.tools import SLACK_TOOLS, create_slack_handler
from api.apps.github.models import GitHubCredential
from api.models import SlackCredentials as SlackCredential
import secrets
from datetime import datetime, timedelta
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["tools"]
)

# Tool registry with all available tools
TOOL_REGISTRY = {
    "github": GITHUB_TOOLS, 
    "slack": SLACK_TOOLS
    # Add more app tools here as they are implemented
}

# Registry of app-specific tool handlers and factory functions
APP_HANDLER_FACTORIES = {}

# Define a function to register app handlers
def register_app_handler(app_name, handler_factory):
    """Register an app handler factory function
    
    Args:
        app_name (str): The name of the app
        handler_factory (callable): Function that creates a handler for the app
    """
    APP_HANDLER_FACTORIES[app_name] = handler_factory

# Register the GitHub handler from the GitHub module
register_app_handler("github", create_github_handler)

# Register the Slack handler from the Slack module
register_app_handler("slack", create_slack_handler)

@router.get("/apps/{app}/tools/", response_model=List[schemas.Tool])
async def list_app_tools(app: str, db: Session = Depends(database.get_db)):
    """List all tools available for a specific app
    
    Args:
        app (str): App name (e.g., 'github')
        db (Session): Database session
        
    Returns:
        List[schemas.Tool]: List of tools for the app
    """
    if app not in TOOL_REGISTRY:
        return []
        
    app_tools = TOOL_REGISTRY[app]
    return [schemas.Tool(
        name=tool_def["name"],
        description=tool_def["description"],
        parameters=tool_def["parameters"]
    ) for tool_def in app_tools.values()]


@router.get("/apps/{app}/tools/{tool}/", response_model=schemas.Tool)
async def get_tool(app: str, tool: str, db: Session = Depends(database.get_db)):
    """Get a specific tool by app and tool name
    
    Args:
        app (str): App name (e.g., 'github')
        tool (str): Tool name (e.g., 'github.list_repos')
        db (Session): Database session
        
    Returns:
        schemas.Tool: Tool details
        
    Raises:
        HTTPException: If tool is not found
    """
    if app not in TOOL_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"App {app} not found"
        )
    
    app_tools = TOOL_REGISTRY[app]
    if tool not in app_tools:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool {tool} not found in app {app}"
        )
    
    tool_def = app_tools[tool]
    return schemas.Tool(
        name=tool_def["name"],
        description=tool_def["description"],
        parameters=tool_def["parameters"]
    )

@router.get("/guess-tools/")
async def guess_tools(description: str, db: Session = Depends(database.get_db)):
    return {"suggested_tools": []}

@router.post("/execute/", response_model=schemas.ExecuteToolResponse)
async def execute_tool(request: schemas.ExecuteToolRequest, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_active_user)):
    """Execute a tool with provided parameters
    
    Args:
        request (schemas.ExecuteToolRequest): Tool execution request
        db (Session): Database session
        current_user (models.User): Current authenticated user
        
    Returns:
        schemas.ExecuteToolResponse: Execution result
        
    Raises:
        HTTPException: If tool is not found or execution fails
    """
    tool_name = request.tool
    parameters = request.parameters if request.parameters else {}
    
    # Extract app name from tool name (e.g., 'github.list_repos' -> 'github')
    app_name = tool_name.split('.')[0] if '.' in tool_name else ''
    
    logger.info(f"Executing tool: {tool_name} for user {current_user.id}")
    
    try:
        # Check if app is supported
        if app_name not in APP_HANDLER_FACTORIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported app: {app_name}"
            )
        
        # Check if the tool exists in the registry
        if app_name in TOOL_REGISTRY and tool_name not in TOOL_REGISTRY[app_name]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_name} not found for app {app_name}"
            )
        
        # Get the appropriate handler for this app
        handler_factory = APP_HANDLER_FACTORIES[app_name]
        handler = handler_factory(current_user.id, db)
        
        # Execute the tool using the handler
        result = handler.execute_tool(tool_name, parameters)
        
        # Log successful execution
        logger.info(f"Successfully executed {tool_name}")
        
        return {
            "success": True,
            "result": result
        }
    
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        # Log and handle other exceptions
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/tools/{tool_id}/execute/", response_model=schemas.ExecuteToolResponse)
async def execute_specific_tool(tool_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_active_user)):
    """Execute a tool by its ID
    
    Args:
        tool_id (int): Tool ID in the database
        db (Session): Database session
        current_user (models.User): Current authenticated user
        
    Returns:
        schemas.ExecuteToolResponse: Execution result
    """
    # For now, this is a placeholder. In a future implementation, we would:  
    # 1. Look up the tool by ID in the database
    # 2. Get the tool handler for the associated app
    # 3. Execute the tool with the provided parameters
    
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool with id {tool_id} not found"
        )
        
    # For now, return a mock response
    return {"success": True, "result": {"message": f"Tool {tool_id} execution not implemented yet"}}

@router.post("/execute/log/{execution_log_id}/rate/")
async def rate_execution(execution_log_id: int, rating: int, db: Session = Depends(database.get_db)):
    return {"status": "success"}

@router.get("/tools/", response_model=List[schemas.Tool])
async def list_tools(db: Session = Depends(database.get_db)):
    return []

@router.get("/mcp-url/", response_model=schemas.MCPUrlResponse)
async def generate_mcp_url(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_active_user)):
    """Generate a unique URL for the user to connect their MCP client
    
    This URL contains authentication information that allows the MCP client
    to access all tools available to the user without additional authentication.
    
    Args:
        db (Session): Database session
        current_user (models.User): Current authenticated user
        
    Returns:
        schemas.MCPUrlResponse: MCP URL and associated metadata
    """
    try:
        # Log the URL generation request
        logger.info(f"Generating MCP URL for user {current_user.id}")
        
        # Get available apps for the user
        available_apps = []
        for app_name in APP_HANDLER_FACTORIES.keys():
            # Check if the user has credentials for this app
            # This would be replaced with actual credential checking logic
            app_available = False
            
            if app_name == "github":
                # Check if user has GitHub credentials
                github_creds = db.query(GitHubCredential).filter(
                    GitHubCredential.user_id == current_user.id
                ).first()
                app_available = github_creds is not None
            
            elif app_name == "slack":
                # Check if user has Slack credentials
                slack_creds = db.query(SlackCredential).filter(
                    SlackCredential.user_id == current_user.id
                ).first()
                app_available = slack_creds is not None
            
            if app_available:
                available_apps.append(app_name)
        
        # Generate a token for the user that includes access to their apps
        # In a real implementation, this would be a JWT or similar token with appropriate expiration
        
        # Generate a secure random token
        token = secrets.token_hex(32)
        
        # Create an expiration date (24 hours from now)
        expires_at = datetime.utcnow() + timedelta(days=1)
        
        # Store the token in the database associated with this user
        # This is a simplified version - in a real app you'd store this securely
        new_token = models.MCPToken(
            user_id=current_user.id,
            token=token,
            expires_at=expires_at
        )
        db.add(new_token)
        db.commit()
        
        # Construct the MCP URL with the token
        # In a real application, this would be properly configured based on deployment environment
        base_url = os.environ.get("MCP_URL_BASE", "http://localhost:8000/api/v1/mcp")
        mcp_url = f"{base_url}?token={token}"
        
        return {
            "url": mcp_url,
            "expires_at": expires_at,
            "description": f"MCP URL with access to these apps: {', '.join(available_apps)}"
        }
        
    except Exception as e:
        logger.error(f"Error generating MCP URL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate MCP URL"
        )

@router.get("/tools/{tool_id}/", response_model=schemas.Tool)
async def get_tool_by_id(tool_id: int, db: Session = Depends(database.get_db)):
    return {}
