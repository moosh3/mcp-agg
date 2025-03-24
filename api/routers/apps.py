from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from api import schemas, database
from api.dependencies import get_current_user
from api.apps import crud as apps_crud

router = APIRouter(
    tags=["apps"]
)

@router.get("/apps", response_model=List[Dict[str, Any]])
async def list_available_apps():
    """List all apps available for registration.
    
    Returns a list of all apps that can be registered by users.
    This is not restricted by authentication since it's informational.
    """
    return apps_crud.get_available_apps()

@router.get("/user/apps", response_model=List[schemas.App])
async def list_user_apps(current_user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    """List all apps registered by the authenticated user.
    
    Returns a list of apps that the current user has registered.
    """
    return apps_crud.get_user_apps(db, current_user.id)

@router.post("/user/apps", response_model=schemas.App, status_code=status.HTTP_201_CREATED)
async def register_app(app: schemas.AppCreate, current_user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    """Register a new app for the authenticated user.
    
    This allows a user to register a new app with their credentials.
    """
    return apps_crud.create_app(db, app, current_user.id)

@router.get("/user/apps/{app_id}", response_model=schemas.App)
async def get_user_app(app_id: int, current_user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    """Get details of a specific app registered by the user.
    
    Returns the details of a specific app registered by the authenticated user.
    """
    app = apps_crud.get_app(db, app_id)
    if not app or app.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="App not found")
    return app

@router.delete("/user/apps/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_app(app_id: int, current_user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    """Delete an app registration.
    
    Deletes an app registration for the authenticated user.
    """
    success = apps_crud.delete_app(db, app_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="App not found")
    return {"status": "deleted"}

@router.get("/dashboard/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(current_user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    """Get dashboard statistics for the authenticated user.
    
    Returns statistics about the user's registered apps and available tools.
    """
    # Get user's registered apps
    user_apps = apps_crud.get_user_apps(db, current_user.id)
    
    # Get all available apps
    available_apps = apps_crud.get_available_apps()
    
    # Count total tools across all user's apps
    total_tools = sum(len(app.tools) for app in user_apps)
    
    # Count enabled tools (assuming all tools are enabled for now)
    enabled_tools = total_tools
    
    return {
        "totalApps": len(available_apps),
        "configuredApps": len(user_apps),
        "totalTools": total_tools,
        "enabledTools": enabled_tools
    }
