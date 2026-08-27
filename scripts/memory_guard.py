#!/usr/bin/env python3
"""Memory firewall — 用 git 管理 Claude Code 的项目记忆目录，
在每次 pipeline 运行前后做隔离与审计。

背景：
- 会话不再用 --bare（--bare 会连同 PreToolUse hooks 一起跳过，
  使 path_guard 文件封锁失效）。auto-memory 注入改由本脚本阻断：
  quarantine 模式下，pre_run 记录基线后**清空记忆目录工作树**，
  运行期间会话即使触发 auto-memory 也读不到任何"前世记忆"；
  post_run 把运行期间的改动捕获进 git 历史，再恢复基线。
- 除主项目记忆目录外，每个题目工作区还有自己的记忆 slug
  （~/.claude/projects/<workspace-slug>/memory/，按 cwd 路径生成）——
  sub-agent 的 cwd 是 workspace，所以这个目录同样在防守范围内。
- 除 auto-memory 外，Agent 也可能用工具直接读写记忆文件：
  直接文件访问由 scripts/path_guard.py（PreToolUse hook）硬拦截，
  本脚本负责运行窗口内的清空/捕获/恢复与审计。

用法：
    python3 scripts/memory_guard.py status              # 查看记忆目录状态
    python3 scripts/memory_guard.py baseline            # 把当前状态固化为新基线
    python3 scripts/memory_guard.py pre  <workspace>    # run.py 运行前调用
    python3 scripts/memory_guard.py post <workspace>    # run.py 运行后调用
    python3 scripts/memory_guard.py restore             # 意外中断后从历史恢复基线

配置（config.json 顶层）：
    "memory_guard": "quarantine" | "audit" | "off"     （默认 quarantine）

注意：记忆目录也是交互式会话的记忆所在地。quarantine 只会在 pipeline 运行
窗口内清空/重置改动，且所有改动都先提交进 git 历史——没有任何东西会被真正删除。
"""

import sys, os, re, json, shutil, subprocess, time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
CONFIG = json.loads((PROJECT_ROOT / "config.json").read_text(encoding="utf-8"))
MODE = CONFIG.get("memory_guard", "quarantine")
GIT_USER = ("memory-guard@physics-solver", "Memory Guard")


def memory_dir(project_root=PROJECT_ROOT):
    """Claude Code 项目记忆目录：~/.claude/projects/<slug>/memory/。"""
    slug = re.sub(r"[^a-zA-Z0-9]", "-", str(project_root))
    return Path.home() / ".claude" / "projects" / slug / "memory"


def memory_dirs(workspace):
    """防守范围：主项目记忆目录 + 该工作区的专属记忆目录（按 cwd slug）。"""
    dirs = [memory_dir()]
    if workspace:
        ws_dir = memory_dir(Path(workspace).resolve())
        if ws_dir != dirs[0]:
            dirs.append(ws_dir)
    return dirs


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


def clear_worktree(mem):
    """删除记忆目录工作树中的全部文件（保留 .git），并提交。"""
    for entry in os.listdir(mem):
        if entry == ".git":
            continue
        p = os.path.join(mem, entry)
        if os.path.isdir(p) and not os.path.islink(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            try:
                os.remove(p)
            except OSError:
                pass
    commit_all(mem, f"memory_guard: cleared for run "
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')}")


def pre_run(workspace, mode=MODE):
    """运行前：归档待提交改动，记录基线；quarantine 模式清空工作树。

    返回报告 dict，其中 baselines = {记忆目录: 基线 sha}（供 post_run 恢复）。
    """
    report = {"mode": mode, "memory_dir": str(memory_dir()), "skipped": False,
              "baselines": {}}
    if mode == "off":
        report["skipped"] = True
        return report
    try:
        any_dir = False
        for mem in memory_dirs(workspace):
            # 工作区专属记忆目录可能尚不存在：主动创建，使其拥有"空基线"，
            # 运行期间写入的记忆才能在 post_run 被捕获并重置（而不是被当成基线）
            try:
                mem.mkdir(parents=True, exist_ok=True)
            except OSError:
                continue
            if not ensure_repo(mem):
                continue
            any_dir = True
            # 交互式会话留下的未提交改动：归档为捕获提交（保留在历史中）。
            commit_all(mem, f"memory_guard: pre-run capture ({workspace}) "
                            f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
            baseline = head_sha(mem)
            if mode == "quarantine":
                # 清空工作树：运行期间 auto-memory 注入找不到任何内容，
                # "前世记忆"无法进入解题过程（改动均已提交，可恢复）。
                clear_worktree(mem)
            # baseline = 运行前真实状态（恢复目标）；clean = 运行开始时的状态
            # （清空后，用于判断运行期间是否有改动）
            report["baselines"][str(mem)] = {"baseline": baseline,
                                             "clean": head_sha(mem)}
            report.setdefault("baseline", baseline)
        if not any_dir:
            report["skipped"] = True
            report["note"] = "memory dir absent"
    except Exception as e:
        report["skipped"] = True
        report["error"] = str(e)[:200]
    return report


def post_run(workspace, baseline=None, baselines=None, mode=MODE):
    """运行后：归档运行期间的改动；quarantine 模式重置回基线。返回报告 dict。

    baselines 优先（pre_run 的完整报告，覆盖主目录与工作区目录）；
    只传 baseline 时仅处理主目录（向后兼容）。
    """
    mem_main = memory_dir()
    report = {"mode": mode, "memory_dir": str(mem_main), "skipped": False,
              "changed": False}
    if mode == "off":
        report["skipped"] = True
        return report
    if baselines is None:
        baselines = {str(mem_main): baseline} if baseline else {}
    try:
        any_dir = False
        for mem in memory_dirs(workspace):
            if not ensure_repo(mem):
                continue
            any_dir = True
            info = baselines.get(str(mem)) or {}
            if isinstance(info, str):
                # 向后兼容：单个 sha 既是恢复点也是运行开始状态
                info = {"baseline": info, "clean": info}
            restore_to = info.get("baseline")
            clean = info.get("clean", restore_to)
            captured = commit_all(mem, f"memory_guard: pipeline capture ({workspace}) "
                                       f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
            head = head_sha(mem)
            # 与"运行开始状态"比较（quarantine 下那是清空后的提交，
            # 不能与运行前基线比——否则每次都会误报有改动）
            if bool(captured) or (clean and head != clean) or is_dirty(mem):
                report["changed"] = True
                report.setdefault("captures", []).append(str(mem))
            if mode == "quarantine" and restore_to:
                # 无条件恢复到运行前基线：quarantine 清空过工作树，
                # 不恢复的话运行结束后记忆目录会停留在清空状态。
                # read-tree 同时处理"新增文件"（基线中不存在的会被移除）
                _git(mem, "read-tree", "--reset", "-u", restore_to, check=True)
                commit_all(mem, f"memory_guard: restore baseline {restore_to} ({workspace})")
                report["reset_to"] = restore_to
        if not any_dir:
            report["skipped"] = True
        report["head"] = head_sha(mem_main)
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
    elif cmd == "restore":
        # 安全网：若运行中途崩溃导致记忆目录停留在"已清空"状态，
        # 从 git 历史恢复——取最近一个"运行前"提交（基线仍在历史里）。
        for mem in memory_dirs(None):
            if not (mem / ".git").exists():
                continue
            r = _git(mem, "log", "--oneline", "--all", "-50")
            target = None
            for line in r.stdout.splitlines():
                if "pre-run capture" in line or "reset to baseline" in line \
                        or "initial baseline" in line or "manual baseline" in line:
                    target = line.split()[0]
                    break
            if target:
                _git(mem, "read-tree", "--reset", "-u", target, check=True)
                print(f"{mem}: restored to {target}")
            else:
                print(f"{mem}: no baseline commit found")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
