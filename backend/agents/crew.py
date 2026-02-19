"""
CrewAI Crew Orchestrator — All 6 agents + retry loop + score calculator
"""

import os
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from tools.repo_tools import clone_repo_tool, discover_test_files_tool, read_file_tool, write_file_tool
from tools.test_tools import run_tests_tool, parse_test_failures_tool
from tools.git_tools import create_branch_tool, commit_and_push_tool, get_commit_count_tool
from tools.github_tools import monitor_cicd_tool, get_workflow_status_tool
from tools.analysis_tools import analyze_code_tool, generate_fix_tool

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

def create_repo_analyst():
    return Agent(
        role="Repository Analyst",
        goal="Clone the given GitHub repository and thoroughly analyze its structure. Discover ALL test files dynamically — never hardcode file paths.",
        backstory="You are an expert DevOps engineer who specializes in understanding codebases. You know how to find test files by looking for patterns like test_*.py, *_test.py, *.test.js, *.spec.ts, and test directories.",
        tools=[clone_repo_tool, discover_test_files_tool, read_file_tool],
        llm=llm, verbose=True, allow_delegation=False,
    )

def create_test_runner():
    return Agent(
        role="Test Runner",
        goal="Run all test files in the repository and collect EVERY failure with exact file names, line numbers, and error messages.",
        backstory="You are a QA automation expert who knows how to run pytest, jest, mocha, unittest, and other test frameworks.",
        tools=[run_tests_tool, parse_test_failures_tool],
        llm=llm, verbose=True, allow_delegation=False,
    )

def create_bug_classifier():
    return Agent(
        role="Bug Classifier",
        goal="Analyze all test failures and classify each bug as exactly one of: LINTING, SYNTAX, LOGIC, TYPE_ERROR, IMPORT, or INDENTATION with exact file path and line number.",
        backstory="You are a senior software engineer who instantly recognizes bug types based on error messages and stack traces.",
        tools=[analyze_code_tool, read_file_tool],
        llm=llm, verbose=True, allow_delegation=False,
    )

def create_code_fixer():
    return Agent(
        role="Code Fixer",
        goal="Generate correct, minimal fixes for each classified bug. Fix only what is broken — do not refactor or change unrelated code.",
        backstory="You are an expert programmer who writes clean, minimal fixes and never introduces new bugs while fixing existing ones.",
        tools=[read_file_tool, write_file_tool, generate_fix_tool, analyze_code_tool],
        llm=llm, verbose=True, allow_delegation=False,
    )

def create_git_committer():
    return Agent(
        role="Git Committer",
        goal="Commit all applied fixes with the [AI-AGENT] prefix. Push ONLY to the designated feature branch — NEVER to main. Batch related fixes to minimize commit count.",
        backstory="You are a DevOps engineer who always uses the [AI-AGENT] prefix and never accidentally pushes to protected branches.",
        tools=[create_branch_tool, commit_and_push_tool, get_commit_count_tool],
        llm=llm, verbose=True, allow_delegation=False,
    )

def create_ci_monitor():
    return Agent(
        role="CI/CD Monitor",
        goal="Monitor the GitHub Actions CI/CD pipeline after each push. Report pass/fail status and track all runs with timestamps.",
        backstory="You are a DevOps specialist who deeply understands GitHub Actions and knows how to poll the GitHub API for workflow run status.",
        tools=[monitor_cicd_tool, get_workflow_status_tool],
        llm=llm, verbose=True, allow_delegation=False,
    )

def create_tasks(agents, run_config):
    repo_url = run_config["repo_url"]
    branch_name = run_config["branch_name"]

    task_clone = Task(
        description=f"Clone the GitHub repository at: {repo_url}\nDiscover ALL test files dynamically.\nReturn: repo local path, list of all test files found, directory structure.",
        expected_output='JSON: {"repo_path": str, "test_files": [str], "structure": str}',
        agent=agents["repo_analyst"],
    )

    task_run_tests = Task(
        description="Run ALL discovered tests. Collect every failure with file, line number, and error message.",
        expected_output='JSON: {"total_tests": int, "total_failures": int, "failures": [{file, line, error_message, test_name}]}',
        agent=agents["test_runner"],
        context=[task_clone],
    )

    task_classify = Task(
        description="Classify each failure as: LINTING, SYNTAX, LOGIC, TYPE_ERROR, IMPORT, or INDENTATION with file, line, description, fix_hint.",
        expected_output='JSON list: [{file, line, bug_type, description, fix_hint}]',
        agent=agents["bug_classifier"],
        context=[task_run_tests],
    )

    task_fix = Task(
        description="Generate and apply minimal fixes for each classified bug. Record file, line, bug_type, fix_applied, status ('Fixed' or 'Failed').",
        expected_output='JSON list: [{file, line, bug_type, fix_applied, status, commit_message}]',
        agent=agents["code_fixer"],
        context=[task_classify],
    )

    task_commit = Task(
        description=f"Create branch EXACTLY: {branch_name}\nCommit all fixed files.\nMANDATORY: Each commit message MUST start with '[AI-AGENT]'\nExample: '[AI-AGENT] fix: remove unused import in src/utils.py line 15'\nPush to GitHub.",
        expected_output='JSON: {"branch_name": str, "commits": [str], "total_commits": int, "push_status": str}',
        agent=agents["git_committer"],
        context=[task_fix],
    )

    task_monitor = Task(
        description="Monitor GitHub Actions CI/CD pipeline after push. Poll until complete. Record run_number, status, timestamp.",
        expected_output='JSON: {"final_status": "PASSED"|"FAILED", "cicd_runs": [{iteration, status, timestamp, duration_seconds}], "total_iterations": int}',
        agent=agents["ci_monitor"],
        context=[task_commit],
    )

    return [task_clone, task_run_tests, task_classify, task_fix, task_commit, task_monitor]

def calculate_score(run_data):
    base = 100
    speed_bonus = 0
    efficiency_penalty = 0

    if run_data.get("started_at") and run_data.get("completed_at"):
        start = datetime.fromisoformat(run_data["started_at"])
        end = datetime.fromisoformat(run_data["completed_at"])
        if (end - start).total_seconds() < 300:
            speed_bonus = 10

    total_commits = run_data.get("total_commits", 0)
    if total_commits > 20:
        efficiency_penalty = (total_commits - 20) * 2

    return {
        "base_score": base,
        "speed_bonus": speed_bonus,
        "efficiency_penalty": efficiency_penalty,
        "total_score": max(0, base + speed_bonus - efficiency_penalty),
    }

def run_healing_crew(run_id, repo_url, team_name, leader_name, branch_name, progress_callback=None, max_retries=None):
    max_retries = max_retries or int(os.getenv("MAX_RETRIES", 5))
    run_config = {"run_id": run_id, "repo_url": repo_url, "team_name": team_name, "leader_name": leader_name, "branch_name": branch_name, "max_retries": max_retries}

    agents = {
        "repo_analyst": create_repo_analyst(),
        "test_runner": create_test_runner(),
        "bug_classifier": create_bug_classifier(),
        "code_fixer": create_code_fixer(),
        "git_committer": create_git_committer(),
        "ci_monitor": create_ci_monitor(),
    }

    tasks = create_tasks(agents, run_config)
    crew = Crew(agents=list(agents.values()), tasks=tasks, process=Process.sequential, verbose=True)

    cicd_runs = []
    all_fixes = []
    total_commits = 0
    final_status = "FAILED"
    started_at = datetime.utcnow().isoformat()

    for iteration in range(1, max_retries + 1):
        print(f"\n{'='*60}\n🔄 ITERATION {iteration}/{max_retries}\n{'='*60}\n")
        result = crew.kickoff(inputs=run_config)
        parsed = parse_crew_result(result, run_config)

        all_fixes.extend(parsed.get("fixes", []))
        total_commits += parsed.get("total_commits", 0)
        cicd_runs.append({
            "iteration": iteration,
            "status": parsed.get("ci_status", "FAILED"),
            "timestamp": datetime.utcnow().isoformat(),
            "duration_seconds": parsed.get("ci_duration", 0),
        })

        if parsed.get("ci_status") == "PASSED":
            final_status = "PASSED"
            break

    completed_at = datetime.utcnow().isoformat()
    final_result = {
        "run_id": run_id, "repo_url": repo_url, "team_name": team_name,
        "leader_name": leader_name, "branch_name": branch_name,
        "started_at": started_at, "completed_at": completed_at,
        "status": "COMPLETED", "final_ci_status": final_status,
        "total_fixes": len(all_fixes), "total_commits": total_commits,
        "fixes": all_fixes, "cicd_runs": cicd_runs,
        "total_iterations": len(cicd_runs), "max_retries": max_retries,
    }
    final_result["score"] = calculate_score(final_result)
    return final_result

def parse_crew_result(result, run_config):
    import json, re
    result_str = str(result)
    json_matches = re.findall(r'\{[^{}]*\}|\[[^\[\]]*\]', result_str, re.DOTALL)
    fixes, ci_status, total_commits, ci_duration = [], "UNKNOWN", 0, 0
    for match in json_matches:
        try:
            data = json.loads(match)
            if isinstance(data, list) and data and "bug_type" in data[0]:
                fixes = data
            elif isinstance(data, dict):
                if "final_status" in data:
                    ci_status = data["final_status"]
                    ci_duration = data.get("duration_seconds", 0)
                if "total_commits" in data:
                    total_commits = data["total_commits"]
        except Exception:
            pass
    return {"fixes": fixes, "ci_status": ci_status, "total_commits": total_commits, "ci_duration": ci_duration}