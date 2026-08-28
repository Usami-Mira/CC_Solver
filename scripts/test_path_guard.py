#!/usr/bin/env python3
"""Unit tests for scripts/path_guard.py (PreToolUse hook)."""
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / "scripts" / "path_guard.py"

ok = []
def check(name, cond, detail=""):
    ok.append(bool(cond))
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {detail}" if detail and not cond else ""))

def call(tool, tool_input, workspace, role=None, cwd=None, extra_env=None):
    env = os.environ.copy()
    if workspace is not None:
        env["WORKSPACE"] = str(workspace)
    else:
        env.pop("WORKSPACE", None)
    if role:
        env["WORKSPACE_ROLE"] = role
    if extra_env:
        env.update(extra_env)
    payload = {"tool_name": tool, "tool_input": tool_input}
    if cwd:
        payload["cwd"] = str(cwd)
    r = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload),
                       capture_output=True, text=True, env=env, timeout=30)
    return r.returncode, r.stderr

with tempfile.TemporaryDirectory() as td:
    ws = Path(td) / "prob1"
    (ws / "debug").mkdir(parents=True)
    (ws / "problem.md").write_text("# problem\n")
    (ws / "tasks").mkdir()
    (ws / "tasks" / "task_builder.md").write_text("# task\n")
    other = Path(td) / "prob2"          # 另一个工作区
    other.mkdir()
    (other / "solution.md").write_text("secret of another run\n")
    outside = Path(td) / "outside.txt"  # workspace 之外的普通文件
    outside.write_text("outside\n")
    # workspace 内指向外部文件的符号链接
    link = ws / "sneaky_link"
    link.symlink_to(outside)

    print("-- gate --")
    rc, _ = call("Read", {"file_path": str(outside)}, workspace=None)
    check("no WORKSPACE env → passthrough", rc == 0, f"rc={rc}")

    print("-- structured file tools --")
    rc, _ = call("Read", {"file_path": str(ws / "problem.md")}, ws)
    check("Read inside workspace allowed", rc == 0, f"rc={rc}")
    rc, err = call("Read", {"file_path": str(outside)}, ws)
    check("Read outside workspace denied", rc == 2, f"rc={rc} {err}")
    rc, err = call("Read", {"file_path": str(other / "solution.md")}, ws)
    check("Read sibling workspace denied", rc == 2, f"rc={rc} {err}")
    home_file = Path.home() / ".claude" / "settings.json"
    rc, err = call("Read", {"file_path": str(home_file)}, ws)
    check("Read ~/.claude denied", rc == 2, f"rc={rc} {err}")
    rc, err = call("Read", {"file_path": str(ROOT / "input" / "solution_1.md")}, ws)
    check("Read input/ (standard answers) denied", rc == 2, f"rc={rc} {err}")
    rc, err = call("Read", {"file_path": str(link)}, ws)
    check("Read symlink escaping workspace denied", rc == 2, f"rc={rc} {err}")
    rc, _ = call("Read", {"file_path": str(ROOT / "textbook" / "merged" / "chunks_translated.json")}, ws)
    check("Read textbook/ (RAG) allowed", rc == 0, f"rc={rc}")
    rc, err = call("Write", {"file_path": str(ROOT / "textbook" / "junk.md"), "content": "x"}, ws)
    check("Write into textbook denied (read-only root)", rc == 2, f"rc={rc} {err}")
    rc, err = call("Write", {"file_path": str(ws / "solution.md"), "content": "x"}, ws)
    check("Write inside workspace allowed", rc == 0, f"rc={rc} {err}")
    rc, err = call("Glob", {"pattern": "*", "path": str(ROOT / "input")}, ws)
    check("Glob outside workspace denied", rc == 2, f"rc={rc} {err}")
    rc, _ = call("Grep", {"pattern": "x"}, ws)
    check("Grep without path allowed (defaults to project)", rc == 0, f"rc={rc}")

    print("-- Bash scanning --")
    rc, err = call("Bash", {"command": f"cat {outside}"}, ws)
    check("Bash cat outside denied", rc == 2, f"rc={rc} {err}")
    rc, err = call("Bash", {"command": f"python3 -c \"print(open('{outside}').read())\""}, ws)
    check("Bash quoted path inside python denied", rc == 2, f"rc={rc} {err}")
    rc, err = call("Bash", {"command": "cat $HOME/.claude/settings.json"}, ws)
    check("Bash $HOME expansion denied", rc == 2, f"rc={rc} {err}")
    rc, err = call("Bash", {"command": "cat ~/.claude/settings.json"}, ws)
    check("Bash ~ expansion denied", rc == 2, f"rc={rc} {err}")
    rc, err = call("Bash", {"command": f"cat ../{other.name}/solution.md"}, ws)
    check("Bash relative escape denied", rc == 2, f"rc={rc} {err}")
    rc, err = call("Bash", {"command": "claude -p 'do my homework'"}, ws)
    check("Bash nested claude denied", rc == 2, f"rc={rc} {err}")
    rc, _ = call("Bash", {"command": "python3 scripts/builder/t1/solve.py"}, ws)
    check("Bash workspace-relative script allowed", rc == 0, f"rc={rc}")
    rc, _ = call("Bash", {"command":
        f"cd {ROOT / 'textbook'} && rag_env/bin/python rag_build/query_rag.py 'test'"}, ws)
    check("Bash RAG invocation allowed", rc == 0, f"rc={rc}")
    spawn_cmd = f"python3 {ROOT / 'scripts' / 'spawn.py'} Builder {ws} task_builder task_builder"
    rc, err = call("Bash", {"command": spawn_cmd}, ws, role="orchestrator")
    check("orchestrator may run scripts/spawn.py", rc == 0, f"rc={rc} {err}")
    rc, err = call("Bash", {"command": spawn_cmd}, ws, role="agent")
    check("agent may NOT run scripts/spawn.py", rc == 2, f"rc={rc} {err}")
    rc, _ = call("Bash", {"command": "cat tasks/task_builder.md"}, ws,
                 role="orchestrator", cwd=ROOT)
    check("orchestrator relative tasks/ path resolved against workspace", rc == 0, f"rc={rc}")

    print("-- audit log --")
    audit_log = ws / "debug" / ".path_guard.log"
    content = audit_log.read_text() if audit_log.exists() else ""
    check("audit log exists", audit_log.exists())
    check("audit log records DENY", "DENY" in content, content[:200])
    check("audit log records ALLOW", "ALLOW" in content, content[:200])

print("\n" + ("PATH_GUARD TESTS PASSED" if all(ok) else "PATH_GUARD TESTS FAILED"))
sys.exit(0 if all(ok) else 1)
