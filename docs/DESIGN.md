# MCP Aggregator: API Design Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Core Concepts](#core-concepts)
   - [Users](#users)
   - [Apps](#apps)
   - [Tools](#tools)
4. [Relationship Model](#relationship-model)
5. [Handler Registry Pattern](#handler-registry-pattern)
6. [Authentication Flow](#authentication-flow)
7. [Tool Execution Flow](#tool-execution-flow)
8. [API Endpoints](#api-endpoints)
9. [Adding New App Integrations](#adding-new-app-integrations)

## Introduction

The MCP Aggregator is designed to be a central hub for connecting to and using tools from various applications. This document outlines the design principles, relationships between core entities, and the workflow for executing tools across different integrated applications.

## System Architecture

The system follows a modular architecture with clear separation of concerns:

```
mcp-agg/
├── api/
│   ├── apps/            # App-specific implementations
│   │   ├── github/      # GitHub app integration
│   │   │   ├── client.py    # API client for GitHub
│   │   │   ├── models.py    # Data models for GitHub
│   │   │   ├── routes.py    # API routes for GitHub
│   │   │   ├── schemas.py   # Request/response schemas
│   │   │   ├── tools.py     # Tool definitions and handlers
│   │   │   └── utils.py     # Helper utilities
│   │   └── ... (other apps)
│   ├── auth/            # Authentication components
│   ├── routers/         # Core API routers
│   │   ├── tools.py     # Central tool registry and execution
│   │   └── ...
│   ├── database.py      # Database configuration
│   ├── dependencies.py  # Common dependencies
│   ├── main.py          # FastAPI application setup
│   ├── models.py        # Core data models
│   └── schemas.py       # Core API schemas
```

## Core Concepts

### Users

Users are the primary actors in the system. Each user can:
- Register and authenticate with the MCP system
- Connect to one or more external applications (like GitHub)
- Execute tools from connected applications
- Manage their app credentials and settings

### Apps

Apps represent external services or platforms that provide tools. Each app:
- Requires specific authentication credentials
- Offers a set of tools that can be executed
- Has a dedicated client for API interaction
- Implements a handler for executing its tools

### Tools

Tools are the functionalities provided by apps that users can execute. Each tool:
- Belongs to a specific app
- Has a unique identifier (e.g., "github.list_repos")
- Accepts specific parameters
- Returns results in a structured format

## Relationship Model

```
User (1) --- (*) UserAppCredentials (*) --- (1) App
                         |
                         v
                    Tool Execution
                         |
                         v
App (1) --- (*) Tool --- (*) ToolExecution (*) --- (1) User
```

This model represents the following relationships:

1. A User can connect to multiple Apps through UserAppCredentials
2. An App can have multiple Tools
3. A User can execute multiple Tools through ToolExecution
4. Each ToolExecution is associated with a specific Tool and User

## Handler Registry Pattern

The MCP Aggregator uses a registry pattern for tool handlers to enable scalable integration of multiple apps:

```python
# Registry of app-specific tool handlers and factory functions
APP_HANDLER_FACTORIES = {}

# Function to register an app handler
def register_app_handler(app_name, handler_factory):
    APP_HANDLER_FACTORIES[app_name] = handler_factory

# Tool registry with all available tools
TOOL_REGISTRY = {
    "github": GITHUB_TOOLS
    # Add more app tools here as they are implemented
}
```

This approach provides several benefits:

1. **Scalability**: Adding new apps only requires registering a new handler, without modifying existing code
2. **Separation of Concerns**: Each app handles its own tools independently
3. **Consistency**: Standardized interfaces for tool definitions and execution
4. **Testability**: Easy isolation of app-specific logic for testing

## Authentication Flow

1. User authenticates with the MCP system using JWT
2. User connects to an external app (e.g., GitHub) via OAuth or API keys
3. The system stores the app credentials securely associated with the user
4. When executing tools, the system retrieves the appropriate credentials
5. App-specific clients use these credentials to authenticate API requests

## Tool Execution Flow

1. User requests to execute a tool (e.g., "github.list_repos")
2. System extracts the app name from the tool identifier ("github")
3. System looks up the app handler factory in the registry
4. Factory creates a handler with the user's credentials for that app
5. System validates the tool exists and the parameters are valid
6. Handler executes the tool with the provided parameters
7. Results are returned to the user in a standardized format

```python
async def execute_tool(request):
    tool_name = request.tool
    parameters = request.parameters
    app_name = tool_name.split('.')[0]
    
    # Get the appropriate handler for this app
    handler_factory = APP_HANDLER_FACTORIES[app_name]
    handler = handler_factory(current_user.id, db)
    
    # Execute the tool using the handler
    result = handler.execute_tool(tool_name, parameters)
    
    return {"success": True, "result": result}
```

## API Endpoints

### User Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Authenticate and get JWT token

### App Integration
- `GET /api/v1/apps/` - List available apps
- `GET /api/v1/apps/{app}/` - Get app details
- `POST /api/v1/apps/{app}/connect` - Connect user to an app

### Tool Management
- `GET /api/v1/tools/` - List all available tools
- `GET /api/v1/apps/{app}/tools/` - List tools for a specific app
- `GET /api/v1/apps/{app}/tools/{tool}/` - Get tool details

### Tool Execution
- `POST /api/v1/execute/` - Execute a tool with parameters
- `GET /api/v1/executions/` - List past tool executions

## Adding New App Integrations

To add a new app integration to the MCP Aggregator:

1. Create a new directory under `api/apps/` for the app
2. Implement the required components:
   - `client.py` - API client for the app
   - `models.py` - Data models for the app
   - `schemas.py` - Request/response schemas
   - `tools.py` - Tool definitions and handler
   - `routes.py` - API routes for the app
   - `utils.py` - Helper utilities

3. Define the app's tools in a dictionary (similar to GITHUB_TOOLS)

4. Create a tool handler class for the app:
   ```python
   class NewAppToolHandler:
       def __init__(self, client):
           self.client = client
       
       def execute_tool(self, tool_name, parameters):
           # App-specific tool execution logic
           ...
   ```

5. Create a handler factory function and register it:
   ```python
   def new_app_handler_factory(user_id, db):
       client = get_new_app_client_for_user(user_id, db)
       return NewAppToolHandler(client)
   
   register_app_handler("new_app", new_app_handler_factory)
   ```

6. Add the app's tools to the TOOL_REGISTRY:
   ```python
   TOOL_REGISTRY["new_app"] = NEW_APP_TOOLS
   ```

7. Include the app's router in the main application

By following this pattern, new app integrations can be added without modifying the core execution logic, ensuring a scalable and maintainable architecture.
