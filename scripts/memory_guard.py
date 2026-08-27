#!/usr/bin/env python3
"""Memory firewall — 用 git 管理 Claude Code 的项目记忆目录，
在每次 pipeline 运行前后做隔离与审计。

背景：
- 子 Agent 以 --bare 运行，auto-memory 注入已关闭（claude --help: --bare skips
  auto-memory）。但 Agent 仍可能通过 Read/Write 工具主动读写记忆文件：
  * 读到上次解题留下的"前世记忆" → 答案来源不可信；
  * 把本次题目内容写进记忆 → 污染未来运行。
- 本脚本把记忆目录 git 化，运行前记录基线，运行后审计差异；
  quarantine 模式下，运行期间的任何改动都会被提交为"捕获提交"（永久保留在
  git 历史中，可恢复），然后工作区被重置回基线。

用法：
    python3 scripts/memory_guard.py status              # 查看记忆目录状态
    python3 scripts/memory_guard.py baseline            # 把当前状态固化为新基线
    python3 scripts/memory_guard.py pre  <workspace>    # run.py 运行前调用
    python3 scripts/memory_guard.py post <workspace>    # run.py 运行后调用

配置（config.json 顶层）：
    "memory_guard": "quarantine" | "audit" | "off"     （默认 quarantine）

注意：记忆目录也是交互式会话的记忆所在地。quarantine 只会在 pipeline 运行
窗口内重置改动，且所有改动都先提交进 git 历史——没有任何东西会被真正删除。
"""

import sys, os, re, json, subprocess, time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
CONFIG = json.loads((PROJECT_ROOT / "config.json").read_text(encoding="utf-8"))
MODE = CONFIG.get("memory_guard", "quarantine")
GIT_USER = ("memory-guard@physics-solver", "Memory Guard")


def memory_dir(project_root=PROJECT_ROOT):
    """Claude Code 项目记忆目录：~/.claude/projects/<slug>/memory/。"""
    slug = re.sub(r"[^a-zA-Z0-9]", "-", str(project_root))
    return Path.home() / ".claude" / "projects" / slug / "memory"


def _git(mem, *args, check=False):
    r = subprocess.run(["git", "-C", str(mem)] + list(args),
                       capture_output=True, text=True, timeout=60)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {args[0]} failed: {(r.stderr or r.stdout).strip()[:200]}")
    return r


def ensure_repo(mem):
    """确保记忆目录是 git 仓库；目录不存在则返回 False（无记忆可防守）。"""
    if not mem.is_dir():
        return False
    if not (mem / ".git").exists():
        _git(mem, "init", check=True)
        _git(mem, "config", "user.email", GIT_USER[0], check=True)
        _git(mem, "config", "user.name", GIT_USER[1], check=True)
    commit_all(mem, "memory_guard: initial baseline")
    return True


def head_sha(mem):
    r = _git(mem, "rev-parse", "--short", "HEAD")
    return r.stdout.strip() if r.returncode == 0 else ""


def is_dirty(mem):
    r = _git(mem, "status", "--porcelain")
    return bool(r.stdout.strip())


def commit_all(mem, msg):
    """提交全部改动（含新增/删除）。干净时为空操作，返回 False。"""
    _git(mem, "add", "-A")
    r = _git(mem, "commit", "-m", msg)
    return r.returncode == 0


def pre_run(workspace, mode=MODE):
    """运行前：归档待提交改动，记录基线。返回报告 dict。"""
    mem = memory_dir()
    report = {"mode": mode, "memory_dir": str(mem), "skipped": False}
    if mode == "off":
        report["skipped"] = True
        return report
    try:
        if not ensure_repo(mem):
            report["skipped"] = True
            report["note"] = "memory dir absent"
            return report
        # 交互式会话留下的未提交改动：归档为捕获提交（保留在历史中）。
        # quarantine 模式下，这同时保证运行开始时工作区 == 基线。
        commit_all(mem, f"memory_guard: pre-run capture ({workspace}) "
                        f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
        report["baseline"] = head_sha(mem)
    except Exception as e:
        report["skipped"] = True
        report["error"] = str(e)[:200]
    return report


def post_run(workspace, baseline=None, mode=MODE):
    """运行后：归档运行期间的改动；quarantine 模式重置回基线。返回报告 dict。"""
    mem = memory_dir()
    report = {"mode": mode, "memory_dir": str(mem), "skipped": False, "changed": False}
    if mode == "off":
        report["skipped"] = True
        return report
    try:
        if not ensure_repo(mem):
            report["skipped"] = True
            return report
        captured = commit_all(mem, f"memory_guard: pipeline capture ({workspace}) "
                                   f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
        head = head_sha(mem)
        report["changed"] = bool(captured) or (baseline and head != baseline) or is_dirty(mem)
        if report["changed"] and mode == "quarantine" and baseline:
            # 重置回基线：read-tree 同时处理"新增文件"（基线中不存在的会被移除）
            _git(mem, "read-tree", "--reset", "-u", baseline, check=True)
            commit_all(mem, f"memory_guard: reset to baseline {baseline} ({workspace})")
            report["reset_to"] = baseline
        report["head"] = head_sha(mem)
    except Exception as e:
        report["error"] = str(e)[:200]
    return report


def render(report):
    if report.get("skipped"):
        return f"memory_guard: skipped ({report.get('note') or report.get('error') or report['mode']})"
    parts = [f"memory_guard[{report['mode']}]"]
    if "baseline" in report:
        parts.append(f"baseline={report['baseline']}")
    if "changed" in report:
        parts.append("changed" if report["changed"] else "clean")
    if report.get("reset_to"):
        parts.append(f"reset→{report['reset_to']}")
    if report.get("error"):
        parts.append(f"error: {report['error']}")
    return " ".join(parts)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]

    if cmd == "status":
        mem = memory_dir()
        print(f"memory dir: {mem}")
        if not mem.is_dir():
            print("(不存在 — 无记忆可防守)")
            return
        if (mem / ".git").exists():
            r = _git(mem, "log", "--oneline", "-8")
            print(r.stdout.strip() or "(无提交)")
            print("dirty" if is_dirty(mem) else "clean")
        else:
            print("(尚未 git 化 — 运行一次 pre 即可)")
    elif cmd == "baseline":
        mem = memory_dir()
        if not ensure_repo(mem):
            print("memory dir 不存在，无需操作")
            return
        commit_all(mem, f"memory_guard: manual baseline {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"baseline = {head_sha(mem)}")
    elif cmd == "pre" and len(sys.argv) >= 3:
        print(render(pre_run(sys.argv[2])))
    elif cmd == "post" and len(sys.argv) >= 3:
        print(render(post_run(sys.argv[2])))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
