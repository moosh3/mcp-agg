from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import schemas, database
from api.auth import crud, utils
from api.dependencies import get_current_user, get_current_admin_user

router = APIRouter(
    tags=["authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = utils.verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, payload.get("sub"))
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Register a new user."""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Login to get access token."""
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = utils.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@router.get("/check")
async def check_auth(current_user = Depends(get_current_user)):
    """Check if user is authenticated."""
    return {"status": "authenticated", "user": current_user.email}

@router.get("/accounts")
async def list_accounts(
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 100
):
    """List all user accounts (admin only)."""
    users = crud.get_users(db, skip=skip, limit=limit)
    return {"accounts": users}

@router.patch("/users/{user_id}")
async def update_user_status(
    user_id: int,
    is_active: Optional[bool] = None,
    is_admin: Optional[bool] = None,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(database.get_db)
):
    """Update user status (admin only)."""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = crud.update_user(db, user, is_active=is_active, is_admin=is_admin)
    return updated_user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(database.get_db)
):
    """Delete a user (admin only)."""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    crud.delete_user(db, user)
    return {"status": "success", "message": f"User {user.email} deleted"}
