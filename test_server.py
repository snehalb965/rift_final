#!/usr/bin/env python3
"""
Quick test script to check if the FastAPI server is working
"""

import requests
import json

def test_server():
    base_url = "http://localhost:8000"
    
    print("🔍 Testing FastAPI server...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: API docs
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"✅ API docs: {response.status_code}")
        if response.status_code != 200:
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ API docs failed: {e}")
    
    # Test 3: OpenAPI schema
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        print(f"✅ OpenAPI schema: {response.status_code}")
        if response.status_code == 200:
            schema = response.json()
            print(f"   Title: {schema.get('info', {}).get('title', 'Unknown')}")
    except Exception as e:
        print(f"❌ OpenAPI schema failed: {e}")
    
    # Test 4: List runs endpoint
    try:
        response = requests.get(f"{base_url}/api/runs", timeout=5)
        print(f"✅ API runs endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ API runs endpoint failed: {e}")
    
    return True

if __name__ == "__main__":
    test_server()