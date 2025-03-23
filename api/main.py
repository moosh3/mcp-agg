from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth, tools, health
from api.database import engine, Base
from api.dependencies import get_current_active_user
from api.apps.github.routes import router as github_router
from api.apps.slack.routes import router as slack_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MCP Aggregator",
    description="A centralized location for LLM applications to access external context, tools, and prompts",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
