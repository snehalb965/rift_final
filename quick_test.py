#!/usr/bin/env python3
"""
Quick Test - Test the agent with a simple repository
"""

import sys
import json
sys.path.append('backend')

from backend.simple_agent import simple_healing_agent

def main():
    print("🚀 Quick Agent Test")
    print("=" * 40)
    
    # Test with a simple, reliable repository
    repo_url = "https://github.com/octocat/Hello-World"
    team_name = "RIFT ORGANISERS"
    leader_name = "Saiyam Kumar"
    
    print(f"📂 Repository: {repo_url}")
    print(f"👥 Team: {team_name}")
    print(f"👤 Leader: {leader_name}")
    print(f"🌿 Expected branch: RIFT_ORGANISERS_SAIYAM_KUMAR_AI_Fix")
    print("\n🔄 Running agent...")
    
    try:
        result = simple_healing_agent(repo_url, team_name, leader_name)
        
        print("\n✅ SUCCESS! Agent completed successfully")
        print("=" * 40)
        
        # Key results
        print(f"Status: {result['status']}")
        print(f"Branch: {result['branch_name']}")
        print(f"Total fixes: {result['total_fixes']}")
        print(f"Final CI/CD status: {result.get('final_ci_status', 'UNKNOWN')}")
        
        if result.get('score'):
            print(f"Final score: {result['score']['final_score']}/100")
        
        # Show some fixes if found
        if result['fixes']:
            print(f"\n🔧 Found {len(result['fixes'])} issues:")
            for i, fix in enumerate(result['fixes'][:5], 1):
                print(f"  {i}. {fix['bug_type']} in {fix['file']}:{fix['line_number']}")
        
        # Test JSON serialization
        json_output = json.dumps(result, indent=2, default=str)
        print(f"\n📄 Result is JSON serializable ({len(json_output)} characters)")
        
        # Save result
        with open("quick_test_result.json", "w") as f:
            f.write(json_output)
        print("💾 Result saved to quick_test_result.json")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED! Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Your agent is working! Ready for testing with the dashboard.")
    else:
        print("\n💥 Agent failed. Check the error above and fix before proceeding.")
    
    sys.exit(0 if success else 1)