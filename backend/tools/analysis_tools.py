"""
Analysis Tools — Classify bugs, generate fixes
"""

import json, ast, re
from pathlib import Path
from crewai.tools import tool

def classify_bug_from_message(msg):
    """Classify bug type based on error message patterns."""
    msg = msg.lower()
    checks = [
        ([r"IndentationError", r"unexpected indent", r"unindent does not match"], "INDENTATION"),
        ([r"SyntaxError", r"invalid syntax", r"expected ':'", r"missing ':'"], "SYNTAX"),
        ([r"ImportError", r"ModuleNotFoundError", r"No module named", r"cannot import name"], "IMPORT"),
        ([r"TypeError", r"AttributeError", r"'NoneType'", r"unsupported operand"], "TYPE_ERROR"),
        ([r"unused import", r"imported but unused", r"F401", r"W0611"], "LINTING"),
        ([r"AssertionError", r"assertion failed", r"expected .* but got"], "LOGIC"),
    ]
    for patterns, bug_type in checks:
        for p in patterns:
            if re.search(p, msg, re.IGNORECASE):
                return bug_type
    return "LOGIC"

@tool("Analyze Code for Bugs")
def analyze_code_tool(file_path: str, error_context: str = "") -> str:
    """Analyze a code file for various types of bugs and issues."""
    bugs = []
    try:
        path = Path(file_path)
        if not path.exists():
            return json.dumps({"error": f"File not found: {file_path}"})
        content = path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()

        if file_path.endswith(".py"):
            # Syntax check
            try:
                ast.parse(content)
            except SyntaxError as se:
                bugs.append({"file": file_path, "line": se.lineno or 0, "bug_type": "SYNTAX", "description": f"SyntaxError: {se.msg}", "fix_hint": f"Fix syntax at line {se.lineno}: {se.text}"})

            # Unused imports
            for i, line in enumerate(lines, 1):
                s = line.strip()
                if s.startswith("import ") or s.startswith("from "):
                    parts = s.replace("import ", "IMPORT ").split()
                    if "IMPORT" in parts:
                        idx = parts.index("IMPORT")
                        if idx + 1 < len(parts):
                            name = parts[idx + 1].split(".")[0].strip(",")
                            rest = "\n".join(l for j, l in enumerate(lines, 1) if j != i)
                            if name not in rest:
                                bugs.append({"file": file_path, "line": i, "bug_type": "LINTING", "description": f"Unused import '{name}'", "fix_hint": f"Remove import on line {i}"})

            # Indentation consistency
            indent_type = None
            for i, line in enumerate(lines, 1):
                if line and line[0] in (' ', '\t'):
                    cur = 'tabs' if line[0] == '\t' else 'spaces'
                    if indent_type is None: indent_type = cur
                    elif cur != indent_type:
                        bugs.append({"file": file_path, "line": i, "bug_type": "INDENTATION", "description": f"Mixed indentation", "fix_hint": f"Use consistent {indent_type}"})

            # Missing colons
            for i, line in enumerate(lines, 1):
                s = line.rstrip()
                for kw in ["def ", "class ", "if ", "for ", "while ", "else", "elif ", "try:", "except"]:
                    if s.startswith(kw) and s and not s.endswith(":") and not s.endswith((",","(","\\",)):
                        bugs.append({"file": file_path, "line": i, "bug_type": "SYNTAX", "description": f"Missing colon after '{kw.strip()}'", "fix_hint": f"Add ':' at end of line {i}"})

            if error_context:
                bug_type = classify_bug_from_message(error_context)
                m = re.search(r'line (\d+)', error_context)
                bugs.append({"file": file_path, "line": int(m.group(1)) if m else 0, "bug_type": bug_type, "description": error_context[:200], "fix_hint": f"Fix {bug_type} at line {m.group(1) if m else '?'}", "from_error_context": True})

        return json.dumps({"file": file_path, "bugs_found": len(bugs), "bugs": bugs})
    except Exception as e:
        return json.dumps({"error": str(e), "file": file_path})

@tool("Generate Code Fix")
def generate_fix_tool(file_path: str, line_number: int, bug_type: str, description: str, fix_hint: str) -> str:
    """Generate and apply a code fix for a specific bug."""
    try:
        path = Path(file_path)
        if not path.exists():
            return json.dumps({"success": False, "error": f"File not found: {file_path}"})
        content = path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines(keepends=True)
        if line_number < 1 or line_number > len(lines):
            return json.dumps({"success": False, "error": f"Line {line_number} out of range"})
        original_line = lines[line_number - 1]
        fixed_line = original_line

        if bug_type == "LINTING" and "unused import" in description.lower():
            fixed_line = ""
            fix_desc = f"Removed unused import on line {line_number}"
        elif bug_type == "SYNTAX" and "colon" in fix_hint.lower():
            stripped = original_line.rstrip()
            fixed_line = (stripped + ":\n") if not stripped.endswith(":") else original_line
            fix_desc = f"Added missing colon on line {line_number}"
        elif bug_type == "INDENTATION":
            stripped_left = original_line.lstrip()
            indent = original_line[:len(original_line) - len(stripped_left)]
            fixed_line = indent.replace("\t", "    ") + stripped_left
            fix_desc = f"Normalized indentation on line {line_number}"
        elif bug_type == "IMPORT" and "remove" in fix_hint.lower():
            fixed_line = ""
            fix_desc = f"Removed problematic import on line {line_number}"
        else:
            fix_desc = f"Manual fix needed for {bug_type} on line {line_number}"

        if fixed_line != original_line:
            lines[line_number - 1] = fixed_line
            return json.dumps({"success": True, "file_path": file_path, "line_number": line_number, "bug_type": bug_type, "original_line": original_line, "fixed_line": fixed_line, "fixed_content": "".join(lines), "fix_description": fix_desc, "commit_message": f"fix({bug_type.lower()}): {fix_desc}"})
        return json.dumps({"success": False, "message": "No automatic fix applied — LLM needed", "file_path": file_path, "bug_type": bug_type})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})