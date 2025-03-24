#!/usr/bin/env python

"""
Script to generate an OpenAPI specification file from the FastAPI app without requiring a database connection.
This creates a temporary version of the app that bypasses database initialization.
"""

import json
import os
import sys
import inspect

# Path to save the OpenAPI spec
OPENAPI_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "openapi.json")

# Hack to bypass database connections - we'll monkeypatch SQLAlchemy
import sqlalchemy.engine.base
original_connect = sqlalchemy.engine.base.Engine.connect

# Mock connect function for SQLAlchemy
def mock_connect(self):
    class MockConnection:
        def begin(self):
            class MockTransaction:
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
                def commit(self):
                    pass
                def rollback(self):
                    pass
            return MockTransaction()
        def close(self):
            pass
    return MockConnection()

def main():
    """Generate and save the OpenAPI specification without database connections"""
    print("Setting up SQLAlchemy mock...")
    # Apply the monkey patch
    sqlalchemy.engine.base.Engine.connect = mock_connect
    
    # Now we can safely import the app
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Import the FastAPI App class and dependencies   
    from fastapi import FastAPI, Depends
    from api.routers import auth, tools, health
    from api.dependencies import get_current_active_user
    from api.apps.github.routes import router as github_router
    from api.apps.slack.routes import router as slack_router
    
    print("Creating FastAPI app for OpenAPI schema generation...")
    # Create a new FastAPI app with the same configuration
    app = FastAPI(
        title="MCP Aggregator",
        description="A centralized location for LLM applications to access external context, tools, and prompts",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )
    
    # Include all routers
    app.include_router(
        auth.router,
        prefix="/api/v1",
        tags=["authentication"]
    )

    app.include_router(
        tools.router,
        prefix="/api/v1",
        tags=["tools"],
        dependencies=[Depends(get_current_active_user)]
    )

    app.include_router(
        health.router,
        prefix="/api/v1",
        tags=["health"]
    )

    # Include GitHub router
    app.include_router(
        github_router,
        dependencies=[Depends(get_current_active_user)]
    )

    # Include Slack router
    app.include_router(
        slack_router,
        dependencies=[Depends(get_current_active_user)]
    )
    
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to MCP Aggregator API",
            "docs": "/api/docs",
            "redoc": "/api/redoc",
            "openapi": "/api/openapi.json"
        }
    
    # Generate the OpenAPI schema
    print("Generating OpenAPI schema...")
    openapi_schema = app.openapi()
    
    # Save to file
    print(f"Saving OpenAPI spec to {OPENAPI_FILE}...")
    with open(OPENAPI_FILE, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    print("OpenAPI specification generated successfully!")


if __name__ == "__main__":
    main()
