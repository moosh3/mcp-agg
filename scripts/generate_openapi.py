#!/usr/bin/env python

"""
Script to generate an OpenAPI specification file from the FastAPI app without starting a server.
This extracts the schema directly from the FastAPI app object.
"""

import json
import os
import sys

# Add the parent directory to sys.path to import the api module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app
from api.main import app

# Path to save the OpenAPI spec
OPENAPI_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "openapi.json")


def main():
    """Generate and save the OpenAPI specification directly from the FastAPI app"""
    print("Generating OpenAPI specification...")
    
    # Get the OpenAPI schema as a dict
    openapi_schema = app.openapi()
    
    # Save to file
    print(f"Saving OpenAPI spec to {OPENAPI_FILE}...")
    with open(OPENAPI_FILE, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    print("OpenAPI specification generated successfully!")


if __name__ == "__main__":
    main()
