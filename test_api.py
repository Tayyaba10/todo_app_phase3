#!/usr/bin/env python3
"""
Test script to verify the API endpoints are working correctly after fixes
"""

import requests
import sys
import subprocess
import time

def test_api_endpoints():
    base_url = "http://127.0.0.1:8000"

    print("Testing API endpoints...")

    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root endpoint error: {e}")

    # Test auth endpoints (these should return 422 or 405 for GET, not 404)
    try:
        response = requests.get(f"{base_url}/api/auth/login")
        print(f"Auth login GET: {response.status_code}")
    except Exception as e:
        print(f"Auth login GET error: {e}")

    # Test tasks endpoints (these should return 401 for unauthenticated access, not 404)
    try:
        response = requests.get(f"{base_url}/api/tasks/")
        print(f"Tasks GET: {response.status_code}")
    except Exception as e:
        print(f"Tasks GET error: {e}")

    # Test chat endpoints
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Chat health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Chat health error: {e}")

if __name__ == "__main__":
    print("Starting API test...")
    test_api_endpoints()