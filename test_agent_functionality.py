#!/usr/bin/env python3
"""
RIFT 2026 Agent Functionality Test
Tests the agent with real repositories to verify it works correctly
"""

import json
import time
import sys
import os
sys.path.append('backend')

from backend.simple_agent import simple_healing_agent

def test_repository(repo_url, team_name, leader_name, description):
    """Test the agent with a specific repository"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {description}")
    print(f"📂 Repository: {repo_url}")
    print(f"👥 Team: {team_name} | Leader: {leader_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = simple_healing_agent(repo_url, team_name, leader_name)
        execution_time = time.time() - start_time
        
        print(f"\n✅ Agent completed in {execution_time:.1f}s")
        print(f"📊 Status: {result['status']}")
        print(f"🌿 Branch: {result['branch_name']}")
        print(f"🔧 Total fixes: {result['total_fixes']}")
        print(f"🏆 Final CI/CD status: {result.get('final_ci_status', 'UNKNOWN')}")
        
        if result.get('score'):
            score = result['score']
            print(f"📈 Score: {score['final_score']}/100 (Base: {score['base_score']}, Speed: +{score['speed_bonus']}, Penalty: -{score['efficiency_penalty']})")
        
        # Show sample fixes
        if result['fixes']:
            print(f"\n🔍 Sample fixes found:")
            for i, fix in enumerate(result['fixes'][:3]):  # Show first 3 fixes
                print(f"  {i+1}. {fix['bug_type']} in {fix['file']}:{fix['line_number']}")
                print(f"     → {fix['description']}")
        
        # Show CI/CD runs
        if result.get('cicd_runs'):
            print(f"\n🔄 CI/CD Iterations:")
            for run in result['cicd_runs']:
                status_emoji = "✅" if run['status'] == "PASSED" else "❌"
                print(f"  {status_emoji} Iteration {run['iteration']}: {run['status']}")
        
        return True, result
        
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"\n❌ Agent failed after {execution_time:.1f}s")
        print(f"💥 Error: {str(e)}")
        return False, None

def main():
    """Run comprehensive agent tests"""
    print("🏆 RIFT 2026 Agent Functionality Test")
    print("Testing the agent with various repositories to ensure it works correctly")
    
    # Test repositories with different characteristics
    test_cases = [
        {
            "repo_url": "https://github.com/octocat/Hello-World",
            "team_name": "RIFT ORGANISERS",
            "leader_name": "Saiyam Kumar",
            "description": "Simple test repository (minimal Python code)"
        },
        {
            "repo_url": "https://github.com/pallets/flask",
            "team_name": "Code Warriors",
            "leader_name": "John Doe",
            "description": "Flask framework (large Python project)"
        },
        {
            "repo_url": "https://github.com/psf/requests",
            "team_name": "Python Masters",
            "leader_name": "Jane Smith",
            "description": "Requests library (well-maintained Python project)"
        },
        {
            "repo_url": "https://github.com/python/cpython",
            "team_name": "Core Devs",
            "leader_name": "Guido van Rossum",
            "description": "CPython (very large Python project)"
        }
    ]
    
    results = []
    passed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🚀 Test {i}/{len(test_cases)}")
        
        success, result = test_repository(
            test_case["repo_url"],
            test_case["team_name"], 
            test_case["leader_name"],
            test_case["description"]
        )
        
        results.append({
            "test_case": test_case,
            "success": success,
            "result": result
        })
        
        if success:
            passed += 1
        
        # Add delay between tests to avoid rate limiting
        if i < len(test_cases):
            print("\n⏳ Waiting 5 seconds before next test...")
            time.sleep(5)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}/{len(test_cases)} tests")
    
    if passed == len(test_cases):
        print("🎉 All tests passed! Your agent is working correctly!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    # Save detailed results
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"📄 Detailed results saved to test_results.json")
    
    return passed == len(test_cases)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)