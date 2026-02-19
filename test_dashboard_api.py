#!/usr/bin/env python3
"""
Dashboard API Test - Test the API endpoints that the React dashboard uses
"""

import requests
import json
import time
import sys

API_BASE = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_run_agent_endpoint():
    """Test the run-agent endpoint"""
    print("\n🤖 Testing run-agent endpoint...")
    
    test_payload = {
        "repo_url": "https://github.com/octocat/Hello-World",
        "team_name": "API Test Team",
        "leader_name": "API Test User"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/api/run-agent",
            json=test_payload,
            timeout=10
        )
        
        if response.status_code in [200, 202]:
            data = response.json()
            print(f"✅ Run-agent endpoint working")
            print(f"   Run ID: {data.get('run_id', 'N/A')}")
            print(f"   Branch: {data.get('branch_name', 'N/A')}")
            print(f"   Status: {data.get('status', 'N/A')}")
            return True, data.get('run_id')
        else:
            print(f"❌ Run-agent failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Run-agent error: {e}")
        return False, None

def test_status_endpoint(run_id):
    """Test the status endpoint"""
    if not run_id:
        print("⏭️  Skipping status test (no run_id)")
        return True
    
    print(f"\n📊 Testing status endpoint for run {run_id}...")
    
    try:
        # Wait a bit for the agent to start
        time.sleep(2)
        
        response = requests.get(f"{API_BASE}/api/status/{run_id}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status endpoint working")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Fixes: {data.get('total_fixes', 'N/A')}")
            return True
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
        return False

def test_cors_headers():
    """Test CORS headers for frontend compatibility"""
    print("\n🌐 Testing CORS headers...")
    
    try:
        # Test preflight request
        response = requests.options(
            f"{API_BASE}/api/run-agent",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            },
            timeout=5
        )
        
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
        }
        
        if cors_headers["Access-Control-Allow-Origin"]:
            print("✅ CORS headers present")
            print(f"   Origin: {cors_headers['Access-Control-Allow-Origin']}")
            return True
        else:
            print("❌ CORS headers missing")
            return False
            
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🧪 Dashboard API Test Suite")
    print("=" * 40)
    print("Make sure your backend is running:")
    print("  cd backend && uvicorn main:app --reload")
    print("=" * 40)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("CORS Headers", test_cors_headers),
    ]
    
    passed = 0
    run_id = None
    
    # Run basic tests first
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"💡 Make sure backend is running on {API_BASE}")
    
    # Test run-agent endpoint
    print(f"\n🧪 Run Agent Endpoint")
    success, run_id = test_run_agent_endpoint()
    if success:
        passed += 1
    
    # Test status endpoint
    print(f"\n🧪 Status Endpoint")
    if test_status_endpoint(run_id):
        passed += 1
    
    total_tests = len(tests) + 2  # +2 for run-agent and status
    
    print(f"\n{'=' * 40}")
    print(f"📊 API Test Results: {passed}/{total_tests} passed")
    
    if passed == total_tests:
        print("🎉 All API tests passed! Your backend is ready!")
        print("\n🚀 Next steps:")
        print("1. Start your frontend: cd frontend && npm run dev")
        print("2. Test the full dashboard at http://localhost:5173")
        print("3. Try running the agent with test data from test_data.json")
    else:
        print("⚠️  Some API tests failed. Fix issues before testing dashboard.")
    
    return passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)