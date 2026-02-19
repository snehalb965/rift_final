"""
Git Tools — Branch creation, [AI-AGENT] commits, push safety
"""

import os, json
from pathlib import Path
from crewai.tools import tool

_commit_count = 0
_current_repo_path = ""

@tool("Create Git Branch")
def create_branch_tool(repo_path: str, branch_name: str) -> str:
    """Create a new git branch with protection against creating protected branches."""
    import git
    global _current_repo_path
    protected = {"main", "master", "develop", "dev", "production"}
    if branch_name.lower() in protected:
        return json.dumps({"success": False, "error": f"REFUSED: Cannot create protected branch '{branch_name}'"})
    try:
        repo = git.Repo(repo_path)
        _current_repo_path = repo_path
        if branch_name in [b.name for b in repo.branches]:
            repo.git.checkout(branch_name)
        else:
            repo.git.checkout("-b", branch_name)
        return json.dumps({"success": True, "branch_name": branch_name, "current_branch": repo.active_branch.name})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool("Commit and Push Fixes")
def commit_and_push_tool(repo_path: str, files_changed: str, commit_message: str) -> str:
    """Commit changes with [AI-AGENT] prefix and push to the current branch."""
    import git
    global _commit_count
    try:
        repo = git.Repo(repo_path)
        current_branch = repo.active_branch.name
        if current_branch.lower() in {"main", "master"}:
            return json.dumps({"success": False, "error": f"REFUSED: On protected branch '{current_branch}'"})
        if not commit_message.startswith("[AI-AGENT]"):
            commit_message = f"[AI-AGENT] {commit_message}"
        files = json.loads(files_changed) if isinstance(files_changed, str) else files_changed
        if files:
            for f in files:
                fp = str(Path(repo_path) / f) if not Path(f).is_absolute() else f
                try: repo.index.add([fp])
                except: pass
        else:
            repo.git.add("-A")
        if not repo.index.diff("HEAD") and not repo.untracked_files:
            return json.dumps({"success": True, "message": "Nothing to commit"})
        cw = repo.config_writer()
        cw.set_value("user", "name", "RIFT AI Agent")
        cw.set_value("user", "email", "agent@rift2026.ai")
        cw.release()
        commit = repo.index.commit(commit_message)
        _commit_count += 1
        token = os.getenv("GITHUB_TOKEN", "")
        origin = repo.remotes.origin
        if token and "github.com" in origin.url and "@" not in origin.url:
            origin.set_url(origin.url.replace("https://", f"https://{token}@"))
        push_info = origin.push(refspec=f"{current_branch}:{current_branch}", set_upstream=True)
        push_status = "failed" if any(i.flags & i.ERROR for i in push_info) else "success"
        return json.dumps({"success": True, "commit_hash": commit.hexsha, "commit_message": commit_message, "branch": current_branch, "push_status": push_status, "total_commits_so_far": _commit_count})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool("Get Total Commit Count")
def get_commit_count_tool(repo_path: str) -> str:
    """Get the total number of [AI-AGENT] commits and calculate efficiency penalties."""
    global _commit_count
    try:
        import git
        repo = git.Repo(repo_path)
        agent_commits = [c for c in repo.iter_commits() if "[AI-AGENT]" in c.message]
        count = len(agent_commits)
        _commit_count = count
        return json.dumps({"total_commits": count, "approaching_penalty": count >= 18, "penalty_active": count > 20, "penalty_amount": max(0, (count - 20) * 2)})
    except Exception as e:
        return json.dumps({"total_commits": _commit_count, "error": str(e)})