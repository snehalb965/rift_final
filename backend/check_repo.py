"""
Check what's actually in the Hello-World repository
"""

import tempfile
import git
from pathlib import Path

def check_repo_contents():
    print("🔍 Checking octocat/Hello-World repository contents...")
    
    temp_dir = tempfile.mkdtemp(prefix="check_repo_")
    repo_url = "https://github.com/octocat/Hello-World"
    
    try:
        git.Repo.clone_from(repo_url, temp_dir)
        repo_path = Path(temp_dir)
        
        print(f"📁 Repository cloned to: {temp_dir}")
        print("\n📄 All files in repository:")
        
        for item in repo_path.rglob("*"):
            if item.is_file() and not item.name.startswith('.'):
                rel_path = item.relative_to(repo_path)
                size = item.stat().st_size
                print(f"   - {rel_path} ({size} bytes)")
                
                # Show content of small files
                if size < 1000:
                    try:
                        content = item.read_text(encoding='utf-8', errors='replace')
                        print(f"     Content preview: {content[:100]}...")
                    except:
                        print("     (Binary file)")
        
        print("\n🔍 Looking for better test repositories...")
        
        # Suggest better repositories with actual code and tests
        suggestions = [
            "microsoft/calculator",
            "python/cpython", 
            "pallets/flask",
            "requests/requests"
        ]
        
        print("💡 Better repositories to test with:")
        for repo in suggestions:
            print(f"   - {repo}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_repo_contents()