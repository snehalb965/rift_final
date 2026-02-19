"""
Repo Tools — Clone, discover test files, read/write files
"""

import os, json, tempfile
from pathlib import Path
from crewai.tools import tool

_cloned_repos: dict[str, str] = {}

@tool("Clone GitHub Repository")
def clone_repo_tool(repo_url: str) -> str:
    """Clone a GitHub repository to a temporary directory for analysis."""
    import git
    try:
        temp_dir = tempfile.mkdtemp(prefix="rift_agent_")
        token = os.getenv("GITHUB_TOKEN", "")
        auth_url = repo_url.replace("https://", f"https://{token}@") if token else repo_url
        git.Repo.clone_from(auth_url, temp_dir)
        _cloned_repos["current"] = temp_dir
        return json.dumps({"success": True, "local_path": temp_dir, "repo_name": repo_url.rstrip("/").split("/")[-1]})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool("Discover Test Files")
def discover_test_files_tool(repo_path: str) -> str:
    """Discover all test files in the repository using common patterns."""
    patterns = [
        "test_*.py", "*_test.py", "tests/*.py", "test/*.py",
        "**/test_*.py", "**/*_test.py",
        "*.test.js", "*.spec.js", "*.test.ts", "*.spec.ts",
        "**/*.test.jsx", "**/*.spec.tsx",
        "**/tests/**/*.py", "**/tests/**/*.js",
        "**/__tests__/**/*",
    ]
    root = Path(repo_path)
    found = set()
    for p in patterns:
        for m in root.glob(p):
            if m.is_file():
                found.add(str(m.relative_to(root)))
    for d in root.rglob("test*"):
        if d.is_dir():
            for f in list(d.glob("*.py")) + list(d.glob("*.js")):
                found.add(str(f.relative_to(root)))
    return json.dumps({"test_files": sorted(found), "total_found": len(found), "repo_path": str(root)})

@tool("Read File Contents")
def read_file_tool(file_path: str) -> str:
    """Read the contents of a file with line numbers for analysis."""
    try:
        path = Path(file_path)
        if not path.is_absolute():
            path = Path(_cloned_repos.get("current", ".")) / file_path
        if not path.exists():
            return json.dumps({"error": f"File not found: {file_path}"})
        content = path.read_text(encoding="utf-8", errors="replace")
        numbered = "\n".join(f"{i+1:4d} | {l}" for i, l in enumerate(content.splitlines()))
        return json.dumps({"success": True, "file_path": str(path), "content": content, "numbered_content": numbered, "total_lines": content.count('\n')})
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("Write File Contents")
def write_file_tool(file_path: str, content: str) -> str:
    """Write content to a file, creating directories as needed."""
    try:
        path = Path(file_path)
        if not path.is_absolute():
            path = Path(_cloned_repos.get("current", ".")) / file_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return json.dumps({"success": True, "file_path": str(path), "bytes_written": len(content.encode())})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})