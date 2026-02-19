#!/usr/bin/env python3
"""
RIFT 2026 Hackathon Compliance Test
Verifies that the agent meets all mandatory requirements
"""

import json
import requests
import time
from backend.simple_agent import simple_healing_agent

def test_branch_naming():
    """Test branch naming convention compliance"""
    print("🔧 Testing branch naming convention...")
    
    test_cases = [
        ("RIFT ORGANISERS", "Saiyam Kumar", "RIFT_ORGANISERS_SAIYAM_KUMAR_AI_Fix"),
        ("Code Warriors", "John Doe", "CODE_WARRIORS_JOHN_DOE_AI_Fix"),
        ("Team@123", "User#456", "TEAM_USER_AI_Fix"),
    ]
    
    for team, leader, expected in test_cases:
        result = simple_healing_agent("https://github.com/octocat/Hello-World", team, leader)
        actual = result["branch_name"]
        
        if actual == expected:
            print(f"✅ {team} + {leader} → {actual}")
        else:
            print(f"❌ {team} + {leader} → Expected: {expected}, Got: {actual}")
            return False
    
    return True

def test_bug_detection_format():
    """Test that bug detection matches exact hackathon format"""
    print("🔍 Testing bug detection format...")
    
    # Test with a simple repository
    result = simple_healing_agent("https://github.com/octocat/Hello-World", "TestTeam", "TestUser")
    
    if "fixes" not in result:
        print("❌ No fixes found in result")
        return False
    
    # Check fix format
    for fix in result["fixes"][:3]:  # Check first 3 fixes
        required_fields = ["file", "line_number", "bug_type", "description", "commit_message", "status"]
        
        for field in required_fields:
            if field not in fix:
                print(f"❌ Missing field '{field}' in fix: {fix}")
                return False
        
        # Check description format
        if " → Fix: " not in fix["description"]:
            print(f"❌ Invalid description format: {fix['description']}")
            return False
        
        # Check commit message format
        if not fix["commit_message"].startswith("[AI-AGENT]"):
            print(f"❌ Invalid commit message format: {fix['commit_message']}")
            return False
        
        print(f"✅ Fix format valid: {fix['bug_type']} in {fix['file']}")
    
    return True

def test_score_calculation():
    """Test score calculation system"""
    print("📊 Testing score calculation...")
    
    result = simple_healing_agent("https://github.com/octocat/Hello-World", "TestTeam", "TestUser")
    
    if "score" not in result:
        print("❌ No score found in result")
        return False
    
    score = result["score"]
    required_fields = ["base_score", "speed_bonus", "efficiency_penalty", "final_score"]
    
    for field in required_fields:
        if field not in score:
            print(f"❌ Missing score field: {field}")
            return False
    
    # Verify score logic
    expected_final = score["base_score"] + score["speed_bonus"] - score["efficiency_penalty"]
    if score["final_score"] != expected_final:
        print(f"❌ Score calculation error: Expected {expected_final}, Got {score['final_score']}")
        return False
    
    print(f"✅ Score calculation valid: {score['final_score']} points")
    return True

def test_api_endpoints():
    """Test that API endpoints are working"""
    print("🌐 Testing API endpoints...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        print("✅ Health endpoint working")
        
        # Test run-agent endpoint (just check it exists)
        test_payload = {
            "repo_url": "https://github.com/octocat/Hello-World",
            "team_name": "TestTeam",
            "leader_name": "TestUser"
        }
        
        response = requests.post(
            "http://localhost:8000/api/run-agent",
            json=test_payload,
            timeout=10
        )
        
        if response.status_code not in [200, 202]:
            print(f"❌ Run-agent endpoint failed: {response.status_code}")
            return False
        
        print("✅ Run-agent endpoint working")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API test failed: {e}")
        print("💡 Make sure backend is running: uvicorn main:app --reload")
        return False

def test_results_json_generation():
    """Test that results.json is generated"""
    print("📄 Testing results.json generation...")
    
    result = simple_healing_agent("https://github.com/octocat/Hello-World", "TestTeam", "TestUser")
    
    # Check that result has all required fields for JSON export
    required_fields = [
        "status", "repo_url", "team_name", "leader_name", "branch_name",
        "fixes", "cicd_runs", "score", "started_at", "total_fixes"
    ]
    
    for field in required_fields:
        if field not in result:
            print(f"❌ Missing required field for results.json: {field}")
            return False
    
    # Test JSON serialization
    try:
        json_str = json.dumps(result, indent=2)
        print(f"✅ Results JSON serializable ({len(json_str)} chars)")
        return True
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        return False

def main():
    """Run all compliance tests"""
    print("🏆 RIFT 2026 Hackathon Compliance Test")
    print("=" * 50)
    
    tests = [
        ("Branch Naming Convention", test_branch_naming),
        ("Bug Detection Format", test_bug_detection_format),
        ("Score Calculation", test_score_calculation),
        ("Results JSON Generation", test_results_json_generation),
        ("API Endpoints", test_api_endpoints),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"🏆 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for hackathon submission!")
        return True
    else:
        print("⚠️  Some tests failed. Please fix issues before submission.")
        return False

if __name__ == "__main__":
    main()