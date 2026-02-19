#!/usr/bin/env python3
"""
Test the LLM-Powered Agent
Demonstrates how the agent uses OpenAI GPT to intelligently fix code issues
"""

import sys
import os
sys.path.append('backend')

from backend.llm_agent import llm_healing_agent

def main():
    print("🤖 RIFT 2026 - LLM-Powered Agent Test")
    print("=" * 50)
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OpenAI API key not found!")
        print("💡 Add your OpenAI API key to backend/.env:")
        print("   OPENAI_API_KEY=sk-your-key-here")
        print("\n🔄 Falling back to rule-based analysis...")
    else:
        print("✅ OpenAI API key found - using LLM-powered analysis!")
    
    # Test with a repository that has Python code
    repo_url = "https://github.com/psf/requests"
    team_name = "LLM Test Team"
    leader_name = "AI Agent"
    
    print(f"\n📂 Repository: {repo_url}")
    print(f"👥 Team: {team_name}")
    print(f"👤 Leader: {leader_name}")
    print(f"🌿 Expected branch: LLM_TEST_TEAM_AI_AGENT_AI_Fix")
    print("\n🚀 Running LLM-powered agent...")
    
    try:
        result = llm_healing_agent(repo_url, team_name, leader_name)
        
        print("\n✅ SUCCESS! LLM Agent completed")
        print("=" * 50)
        
        # Key results
        print(f"Status: {result['status']}")
        print(f"Branch: {result['branch_name']}")
        print(f"Total fixes: {result['total_fixes']}")
        print(f"LLM powered: {result['llm_powered']}")
        print(f"Final CI/CD status: {result.get('final_ci_status', 'UNKNOWN')}")
        
        if result.get('score'):
            score = result['score']
            print(f"Final score: {score['final_score']}/100")
            if score.get('llm_bonus', 0) > 0:
                print(f"  🤖 LLM bonus: +{score['llm_bonus']} points!")
        
        # Show LLM-powered fixes
        if result['fixes']:
            print(f"\n🤖 LLM-Powered Fixes Found:")
            llm_fixes = [f for f in result['fixes'] if f.get('llm_powered', False)]
            rule_fixes = [f for f in result['fixes'] if not f.get('llm_powered', False)]
            
            if llm_fixes:
                print(f"  🧠 LLM-detected issues: {len(llm_fixes)}")
                for i, fix in enumerate(llm_fixes[:3], 1):
                    print(f"    {i}. {fix['bug_type']} in {fix['file']}:{fix['line_number']}")
                    print(f"       → {fix['description']}")
            
            if rule_fixes:
                print(f"  🔧 Rule-based issues: {len(rule_fixes)}")
                for i, fix in enumerate(rule_fixes[:2], 1):
                    print(f"    {i}. {fix['bug_type']} in {fix['file']}:{fix['line_number']}")
        
        # Show CI/CD runs
        if result.get('cicd_runs'):
            print(f"\n🔄 CI/CD Iterations:")
            for run in result['cicd_runs']:
                status_emoji = "✅" if run['status'] == "PASSED" else "❌"
                print(f"  {status_emoji} Iteration {run['iteration']}: {run['status']}")
        
        print(f"\n🎯 Key Features Demonstrated:")
        print(f"  ✅ LLM-powered code analysis")
        print(f"  ✅ Intelligent error detection")
        print(f"  ✅ Automated fix generation")
        print(f"  ✅ Exact hackathon format compliance")
        print(f"  ✅ Multi-agent architecture")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED! Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_without_llm():
    """Test the agent without LLM (rule-based only)"""
    print("\n🔧 Testing Rule-Based Mode (No LLM)")
    print("-" * 30)
    
    # Temporarily remove API key to test fallback
    original_key = os.environ.get("OPENAI_API_KEY")
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    try:
        result = llm_healing_agent(
            "https://github.com/octocat/Hello-World",
            "Rule Test",
            "No LLM"
        )
        
        print(f"✅ Rule-based mode works: {result['total_fixes']} fixes found")
        print(f"   LLM powered: {result['llm_powered']}")
        
    finally:
        # Restore API key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key

if __name__ == "__main__":
    print("🧪 Testing both LLM and rule-based modes...\n")
    
    # Test with LLM
    success = main()
    
    # Test without LLM
    test_without_llm()
    
    if success:
        print("\n🎉 LLM Agent is working! Ready for RIFT 2026 submission!")
        print("\n🚀 Next steps:")
        print("1. Make sure your OpenAI API key is in backend/.env")
        print("2. Test the full dashboard with LLM agent")
        print("3. Deploy and submit to hackathon")
    else:
        print("\n💥 Agent failed. Check the error above and fix before proceeding.")
    
    sys.exit(0 if success else 1)