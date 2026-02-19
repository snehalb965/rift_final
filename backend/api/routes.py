"""
API Routes — All HTTP endpoints the React dashboard calls
"""

import os
import json
import uuid
import asyncio
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from pydantic import BaseModel

from simple_agent import simple_healing_agent
from llm_agent import llm_healing_agent

router = APIRouter()
runs: dict[str, dict] = {}

class RunAgentRequest(BaseModel):
    repo_url: str
    team_name: str
    leader_name: str

class RunAgentResponse(BaseModel):
    run_id: str
    branch_name: str
    status: str
    message: str

def build_branch_name(team_name: str, leader_name: str) -> str:
    import re
    team = re.sub(r'[^A-Z0-9_ ]', '', team_name.upper()).replace(' ', '_')
    leader = re.sub(r'[^A-Z0-9_ ]', '', leader_name.upper()).replace(' ', '_')
    return f"{team}_{leader}_AI_Fix"

@router.post("/run-agent", response_model=RunAgentResponse)
async def run_agent(
    request: Request,
    body: RunAgentRequest,
    background_tasks: BackgroundTasks,
):
    # More flexible URL validation
    repo_url = body.repo_url.strip()
    if not (repo_url.startswith("https://github.com/") or repo_url.startswith("http://github.com/")):
        # Try to fix common URL formats
        if repo_url.startswith("github.com/"):
            repo_url = "https://" + repo_url
        elif repo_url.startswith("www.github.com/"):
            repo_url = "https://" + repo_url
        elif "/" in repo_url and not repo_url.startswith("http"):
            # Assume it's a username/repo format
            repo_url = "https://github.com/" + repo_url
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid GitHub URL. Please use format: https://github.com/username/repository"
            )

    run_id = str(uuid.uuid4())[:8]
    branch_name = build_branch_name(body.team_name, body.leader_name)

    runs[run_id] = {
        "run_id": run_id,
        "status": "STARTING",
        "repo_url": repo_url,  # Use the corrected URL
        "team_name": body.team_name,
        "leader_name": body.leader_name,
        "branch_name": branch_name,
        "started_at": datetime.utcnow().isoformat(),
        "completed_at": None,
        "fixes": [],
        "cicd_runs": [],
        "score": None,
        "error": None,
    }

    ws_manager = request.app.state.ws_manager

    background_tasks.add_task(
        execute_agent_run,
        run_id=run_id,
        repo_url=repo_url,  # Use the corrected URL
        team_name=body.team_name,
        leader_name=body.leader_name,
        branch_name=branch_name,
        ws_manager=ws_manager,
    )

    return RunAgentResponse(
        run_id=run_id,
        branch_name=branch_name,
        status="STARTING",
        message=f"Agent started! Branch will be: {branch_name}",
    )

async def execute_agent_run(
    run_id, repo_url, team_name, leader_name, branch_name, ws_manager
):
    async def send_update(event, data):
        runs[run_id].update(data)
        await ws_manager.send_update(run_id, {"event": event, "run_id": run_id, **data})

    try:
        await send_update("STATUS", {"status": "STARTING", "message": "Initializing agent..."})

        # Use the LLM agent for intelligent fixing
        result = await asyncio.to_thread(
            llm_healing_agent,
            repo_url=repo_url,
            team_name=team_name,
            leader_name=leader_name
        )

        # Update the run data with results
        runs[run_id].update(result)
        runs[run_id]["completed_at"] = datetime.utcnow().isoformat()

        save_results(run_id, runs[run_id])
        await send_update("COMPLETED", runs[run_id])

    except Exception as e:
        runs[run_id]["status"] = "ERROR"
        runs[run_id]["error"] = str(e)
        runs[run_id]["completed_at"] = datetime.utcnow().isoformat()
        await send_update("ERROR", {"error": str(e), "status": "ERROR"})

@router.get("/status/{run_id}")
def get_status(run_id: str):
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run not found")
    return runs[run_id]

@router.get("/results/{run_id}")
def get_results(run_id: str):
    if run_id not in runs:
        results_path = Path(f"./results/{run_id}.json")
        if results_path.exists():
            return json.loads(results_path.read_text())
        raise HTTPException(status_code=404, detail="Run not found")
    return runs[run_id]

@router.get("/runs")
def list_runs():
    return list(runs.values())

def save_results(run_id: str, data: dict):
    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)
    results_path = results_dir / f"{run_id}.json"
    with open(results_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Results saved to {results_path}")