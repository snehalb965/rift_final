#!/usr/bin/env python3
"""
Check if all imports in main.py work correctly
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, 'backend')

def check_imports():
    print("🔍 Checking imports...")
    
    try:
        print("  - Loading dotenv...")
        from dotenv import load_dotenv
        load_dotenv()
        print("  ✅ dotenv loaded")
    except Exception as e:
        print(f"  ❌ dotenv failed: {e}")
        return False
    
    try:
        print("  - Loading FastAPI...")
        from fastapi import FastAPI
        print("  ✅ FastAPI loaded")
    except Exception as e:
        print(f"  ❌ FastAPI failed: {e}")
        return False
    
    try:
        print("  - Loading API routes...")
        os.chdir('backend')
        from api.routes import router
        print("  ✅ API routes loaded")
    except Exception as e:
        print(f"  ❌ API routes failed: {e}")
        return False
    
    try:
        print("  - Loading agents...")
        from simple_agent import simple_healing_agent
        from llm_agent import llm_healing_agent
        print("  ✅ Agents loaded")
    except Exception as e:
        print(f"  ❌ Agents failed: {e}")
        return False
    
    print("✅ All imports successful!")
    return True

if __name__ == "__main__":
    check_imports()