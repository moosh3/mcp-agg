from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    apps: List['App'] = []

    class Config:
        from_attributes = True

# App schemas
class AppBase(BaseModel):
    name: str
    description: Optional[str] = None

class AppCreate(AppBase):
    auth_credentials: Dict[str, Any]

class App(AppBase):
    id: int
    owner_id: int
    tools: List['Tool'] = []

    class Config:
        from_attributes = True

# Tool schemas
class ToolBase(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any]
    action_definition: Dict[str, Any]

class ToolCreate(ToolBase):
    app_id: int

class Tool(ToolBase):
    id: int
    app_id: int

    class Config:
        from_attributes = True

# Tool execution schemas
class ExecuteToolRequest(BaseModel):
    tool: str
    parameters: Optional[Dict[str, Any]] = None

class ExecuteToolResponse(BaseModel):
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# MCP URL generation schema
class MCPUrlResponse(BaseModel):
    url: str
    expires_at: Optional[datetime] = None
    description: str = "URL for connecting to the MCP server with your credentials"

# Update forward references
User.model_rebuild()
App.model_rebuild()
