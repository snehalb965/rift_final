#!/usr/bin/env python3
"""
Demo Script - Shows actual fixes being applied to real code issues
"""

import sys
import os
sys.path.append('backend')

from backend.enhanced_agent import enhanced_healing_agent_demo

def main():
    print("🚀 RIFT 2026 - Live Fix Demonstration")
    print("This will show you actual code issues being detected and fixed!")
    print("\nPress Enter to start the demonstration...")
    input()
    
    try:
        result = enhanced_healing_agent_demo()
        
        print("\n" + "="*60)
        print("🎉 DEMONSTRATION COMPLETE!")
        print("="*60)
        print("You can now see:")
        print("1. Original code with issues")
        print("2. Detected problems with exact line numbers")
        print("3. Applied fixes with before/after comparison")
        print("4. Working corrected code that actually runs")
        
        print(f"\n📂 Check the 'test_repo_with_issues' folder to see all files")
        print("📄 Files created:")
        print("  • utils.py (original with issues)")
        print("  • fixed_utils.py (corrected version)")
        print("  • validator.py (original with issues)")
        print("  • fixed_validator.py (corrected version)")
        print("  • And more...")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Demo successful! Your agent can detect AND fix real issues!")
    else:
        print("\n❌ Demo failed. Check the error above.")
    
    sys.exit(0 if success else 1)