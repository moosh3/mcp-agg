#!/usr/bin/env python

"""
Script to generate an OpenAPI specification file from the FastAPI app.
This script starts the application, fetches the OpenAPI schema, and saves it
to a file in the project root directory.
"""

import json
import os
import sys
import requests
import subprocess
import time
import signal
import atexit

# Add the parent directory to sys.path to import the api module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Path to save the OpenAPI spec
OPENAPI_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "openapi.json")

# URL where FastAPI serves the OpenAPI schema
OPENAPI_URL = "http://localhost:8080/api/openapi.json"

# Uvicorn server process
server_process = None


def cleanup():
    """Cleanup function to shut down the server when script exits"""
    if server_process:
        print("\nShutting down server...")
        os.kill(server_process.pid, signal.SIGTERM)
        server_process.wait()


def start_server():
    """Start the FastAPI server using uvicorn"""
    global server_process
    print("Starting the FastAPI server...")
    server_process = subprocess.Popen(
        ["uv", "python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    atexit.register(cleanup)
    # Wait for server to start up
    time.sleep(3)


def fetch_openapi_spec():
    """Fetch the OpenAPI specification from the FastAPI server"""
    print(f"Fetching OpenAPI spec from {OPENAPI_URL}...")
    try:
        response = requests.get(OPENAPI_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OpenAPI spec: {e}")
        sys.exit(1)


def save_openapi_spec(spec):
    """Save the OpenAPI specification to a file"""
    print(f"Saving OpenAPI spec to {OPENAPI_FILE}...")
    with open(OPENAPI_FILE, "w") as f:
        json.dump(spec, f, indent=2)


def main():
    """Main function to generate the OpenAPI specification"""
    start_server()
    spec = fetch_openapi_spec()
    save_openapi_spec(spec)
    print("OpenAPI specification generated successfully!")


if __name__ == "__main__":
    main()
