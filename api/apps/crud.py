from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from api.models import App, User
from api.schemas import AppCreate

def get_app(db: Session, app_id: int) -> Optional[App]:
    """Get app by ID."""
    return db.query(App).filter(App.id == app_id).first()

def get_available_apps() -> List[dict]:
    """Get list of all available apps that can be registered.
    
    This returns a predefined list of apps available in the system,
    not actual database entries.
    """
    # This is a static list of apps currently supported by the system
    return [
        {
            "id": "github",
            "name": "GitHub",
            "description": "Access GitHub repositories, issues, and pull requests",
            "icon": "github",
            "auth_type": "oauth"
        },
        {
            "id": "slack",
            "name": "Slack",
            "description": "Send messages and interact with Slack channels", 
            "icon": "slack",
            "auth_type": "oauth"
        }
    ]

def get_user_apps(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[App]:
    """Get all apps registered by a specific user."""
    return db.query(App).filter(App.owner_id == user_id).offset(skip).limit(limit).all()

def create_app(db: Session, app: AppCreate, user_id: int) -> App:
    """Create a new app registration for a user."""
    db_app = App(
        name=app.name,
        description=app.description,
        auth_credentials=app.auth_credentials,
        owner_id=user_id,
        created_at=datetime.now()
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def update_app(db: Session, app_id: int, user_id: int, app_data: dict) -> Optional[App]:
    """Update an existing app."""
    db_app = db.query(App).filter(App.id == app_id, App.owner_id == user_id).first()
    if not db_app:
        return None
    
    # Update fields
    for key, value in app_data.items():
        if hasattr(db_app, key):
            setattr(db_app, key, value)
    
    db_app.updated_at = datetime.now()
    db.commit()
    db.refresh(db_app)
    return db_app

def delete_app(db: Session, app_id: int, user_id: int) -> bool:
    """Delete an app registration."""
    db_app = db.query(App).filter(App.id == app_id, App.owner_id == user_id).first()
    if not db_app:
        return False
    
    db.delete(db_app)
    db.commit()
    return True

def check_user_has_app(db: Session, user_id: int, app_name: str) -> bool:
    """Check if a user has a specific app registered by name."""
    return db.query(App).filter(App.owner_id == user_id, App.name == app_name).first() is not None
