"""
GitHub CI/CD Tools — Monitor GitHub Actions, poll workflow status
"""

import os, json, time
from crewai.tools import tool

@tool("Monitor CI/CD Pipeline")
def monitor_cicd_tool(repo_url: str, branch_name: str, max_wait_seconds: int = 300) -> str:
    """Monitor GitHub Actions CI/CD pipeline status and wait for completion."""
    from github import Github
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        return json.dumps({"final_status": "UNKNOWN", "error": "GITHUB_TOKEN not set"})
    try:
        g = Github(token)
        parts = repo_url.rstrip("/").split("/")
        repo = g.get_repo(f"{parts[-2]}/{parts[-1].replace('.git','')}")
        start_time = time.time()
        attempts = []
        time.sleep(15)
        while time.time() - start_time < max_wait_seconds:
            elapsed = time.time() - start_time
            runs = repo.get_workflow_runs(branch=branch_name)
            latest_run = next(iter(runs), None)
            if not latest_run:
                attempts.append({"elapsed_seconds": round(elapsed), "status": "NO_RUNS_YET"})
                time.sleep(30)
                continue
            attempts.append({"elapsed_seconds": round(elapsed), "run_id": latest_run.id, "status": latest_run.status, "conclusion": latest_run.conclusion})
            if latest_run.status == "completed":
                return json.dumps({"final_status": "PASSED" if latest_run.conclusion == "success" else "FAILED", "conclusion": latest_run.conclusion, "run_url": latest_run.html_url, "total_duration_seconds": round(time.time() - start_time), "poll_attempts": attempts, "branch": branch_name})
            time.sleep(30)
        return json.dumps({"final_status": "TIMEOUT", "error": f"CI did not complete within {max_wait_seconds}s", "poll_attempts": attempts})
    except Exception as e:
        return json.dumps({"final_status": "ERROR", "error": str(e)})

@tool("Get Workflow Status")
def get_workflow_status_tool(repo_url: str, branch_name: str) -> str:
    """Get the status of recent GitHub Actions workflow runs for a specific branch."""
    from github import Github
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        return json.dumps({"error": "GITHUB_TOKEN not set"})
    try:
        g = Github(token)
        parts = repo_url.rstrip("/").split("/")
        repo = g.get_repo(f"{parts[-2]}/{parts[-1].replace('.git','')}")
        results = []
        for i, run in enumerate(repo.get_workflow_runs(branch=branch_name)):
            results.append({"run_number": run.run_number, "status": run.status, "conclusion": run.conclusion, "created_at": run.created_at.isoformat(), "url": run.html_url})
            if i >= 4: break
        return json.dumps({"runs": results, "branch": branch_name})
    except Exception as e:
        return json.dumps({"error": str(e)})