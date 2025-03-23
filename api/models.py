from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    apps = relationship("App", back_populates="owner")
    # Reference to GitHubCredential in apps/github/models.py
    github_credentials = relationship("api.apps.github.models.GitHubCredential", back_populates="user", uselist=False)
    slack_credentials = relationship("SlackCredentials", back_populates="user", uselist=False)

class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    auth_credentials = Column(JSON)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed_at = Column(DateTime(timezone=True))
    owner = relationship("User", back_populates="apps")
    tools = relationship("Tool", back_populates="app")

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    app_id = Column(Integer, ForeignKey("apps.id"))
    parameters = Column(JSON)
    action_definition = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_used_at = Column(DateTime(timezone=True))
    app = relationship("App", back_populates="tools")


# GitHubCredential model is defined in api/apps/github/models.py


class SlackCredentials(Base):
    __tablename__ = "slack_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    access_token = Column(String)
    refresh_token = Column(String, nullable=True)
    token_type = Column(String, nullable=True)
    scope = Column(String, nullable=True)
    team_id = Column(String, nullable=True)
    team_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="slack_credentials")


class MCPToken(Base):
    __tablename__ = "mcp_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_revoked = Column(Boolean, default=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    user = relationship("User")
    
    @property
    def is_valid(self):
        """Check if the token is valid (not expired and not revoked)"""
        from datetime import datetime
        return (not self.is_revoked and 
                self.expires_at > datetime.utcnow())
