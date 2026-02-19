"""
Simple test to check if the agent workflow works
"""

import os
import tempfile
import json
from pathlib import Path

def test_simple_workflow():
    print("🔄 Testing simple workflow...")
    
    # Test 1: Clone repository
    print("\n1. Testing repository cloning...")
    try:
        import git
        temp_dir = tempfile.mkdtemp(prefix="test_agent_")
        repo_url = "https://github.com/octocat/Hello-World"
        
        # Clone without authentication first
        git.Repo.clone_from(repo_url, temp_dir)
        print(f"✅ Successfully cloned to: {temp_dir}")
        
        # List files
        repo_path = Path(temp_dir)
        files = list(repo_path.glob("**/*"))
        print(f"📁 Found {len(files)} files:")
        for f in files[:10]:  # Show first 10 files
            if f.is_file():
                print(f"   - {f.name}")
                
    except Exception as e:
        print(f"❌ Clone failed: {e}")
        return False
    
    # Test 2: Find test files
    print("\n2. Testing test file discovery...")
    try:
        test_patterns = ["test_*.py", "*_test.py", "*.test.js"]
        found_tests = []
        
        for pattern in test_patterns:
            for test_file in repo_path.glob(pattern):
                if test_file.is_file():
                    found_tests.append(str(test_file.relative_to(repo_path)))
        
        print(f"🧪 Found {len(found_tests)} test files:")
        for test in found_tests:
            print(f"   - {test}")
            
    except Exception as e:
        print(f"❌ Test discovery failed: {e}")
    
    # Test 3: Check if we can run basic analysis
    print("\n3. Testing basic code analysis...")
    try:
        python_files = list(repo_path.glob("*.py"))
        print(f"🐍 Found {len(python_files)} Python files:")
        
        for py_file in python_files:
            print(f"   - {py_file.name} ({py_file.stat().st_size} bytes)")
            
            # Try to read the file
            content = py_file.read_text(encoding='utf-8', errors='replace')
            lines = len(content.splitlines())
            print(f"     Lines: {lines}")
            
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
    
    print("\n✅ Simple workflow test completed!")
    return True

if __name__ == "__main__":
    test_simple_workflow()