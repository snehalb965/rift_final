"""
Test Tools — Run pytest/jest, parse failures
"""

import os, json, subprocess
from pathlib import Path
from crewai.tools import tool

@tool("Run All Tests")
def run_tests_tool(repo_path: str, test_files: str) -> str:
    """Run all tests in the repository using pytest for Python and jest for JavaScript."""
    try:
        repo = Path(repo_path)
        all_failures, total_tests, total_passed, raw_outputs = [], 0, 0, []

        if any(repo.glob("**/*.py")):
            r = run_pytest(repo_path)
            all_failures.extend(r["failures"]); total_tests += r["total"]; total_passed += r["passed"]; raw_outputs.append(r["raw"])

        if (repo / "package.json").exists():
            r = run_jest(repo_path)
            all_failures.extend(r["failures"]); total_tests += r["total"]; total_passed += r["passed"]; raw_outputs.append(r["raw"])

        return json.dumps({"success": True, "total_tests": total_tests, "total_failures": len(all_failures), "total_passed": total_passed, "failures": all_failures, "raw_output": "\n\n".join(raw_outputs)})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def run_pytest(repo_path):
    timeout = int(os.getenv("SANDBOX_TIMEOUT", 60))
    cmd = ["python", "-m", "pytest", "--tb=short", "-v", "--json-report", "--json-report-file=/tmp/pytest_report.json", repo_path]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=repo_path)
        raw = proc.stdout + proc.stderr
        failures, total, passed = [], 0, 0
        rp = Path("/tmp/pytest_report.json")
        if rp.exists():
            report = json.loads(rp.read_text())
            total = report.get("summary", {}).get("total", 0)
            passed = report.get("summary", {}).get("passed", 0)
            for t in report.get("tests", []):
                if t.get("outcome") == "failed":
                    import re
                    lr = t.get("call", {}).get("longrepr", "")
                    m = re.findall(r'line (\d+)', lr)
                    failures.append({"file": t.get("nodeid","").split("::")[0], "test_name": t.get("nodeid",""), "line": int(m[-1]) if m else 0, "error_message": lr})
        return {"failures": failures, "total": total, "passed": passed, "raw": raw}
    except subprocess.TimeoutExpired:
        return {"failures": [], "total": 0, "passed": 0, "raw": "ERROR: pytest timed out"}

def run_jest(repo_path):
    timeout = int(os.getenv("SANDBOX_TIMEOUT", 60))
    if not (Path(repo_path) / "node_modules").exists():
        subprocess.run(["npm", "install"], capture_output=True, cwd=repo_path, timeout=120)
    try:
        proc = subprocess.run(["npm", "test", "--", "--json", "--no-coverage"], capture_output=True, text=True, timeout=timeout, cwd=repo_path)
        failures, total, passed = [], 0, 0
        try:
            report = json.loads(proc.stdout)
            total = report.get("numTotalTests", 0)
            passed = report.get("numPassedTests", 0)
            for suite in report.get("testResults", []):
                for t in suite.get("testResults", []):
                    if t.get("status") == "failed":
                        failures.append({"file": suite.get("testFilePath",""), "test_name": t.get("fullName",""), "line": 0, "error_message": "\n".join(t.get("failureMessages",[]))})
        except json.JSONDecodeError:
            pass
        return {"failures": failures, "total": total, "passed": passed, "raw": proc.stdout + proc.stderr}
    except subprocess.TimeoutExpired:
        return {"failures": [], "total": 0, "passed": 0, "raw": "ERROR: jest timed out"}

@tool("Parse Test Failures")
def parse_test_failures_tool(raw_output: str) -> str:
    """Parse test output to extract file names, line numbers, and error messages."""
    import re
    failures = []
    for m in re.finditer(r'File "([^"]+)", line (\d+)', raw_output):
        failures.append({"file": m.group(1), "line": int(m.group(2)), "source": "traceback"})
    for m in re.finditer(r'([\w/\\\.]+\.py):(\d+):\s*(.+)', raw_output):
        failures.append({"file": m.group(1), "line": int(m.group(2)), "error_message": m.group(3).strip(), "source": "lint"})
    return json.dumps({"parsed_failures": failures, "total": len(failures)})