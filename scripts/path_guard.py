#!/usr/bin/env python3
"""path_guard — PreToolUse hook：把 pipeline 会话硬锁在 workspace 内。

激活条件：环境变量 WORKSPACE 已设置（由 scripts/run.py 与 scripts/spawn.py
在启动 claude 会话时注入）。未设置时直接放行——交互式会话不受影响。

允许访问的根（allow roots）：
- $WORKSPACE 本身（读写）；
- <project>/textbook（只读：RAG 知识库查询）；
- <project>/scripts（仅 WORKSPACE_ROLE=orchestrator：调用 spawn.py）。

其余一切路径（~/.claude、input/ 标准答案、其它 workspace、项目其余部分）
一律 exit(2) 硬拦截。Bash 命令会被分词扫描，引号内的路径同样会被检查。

已知边界（设计上接受）：base64/变量拼接等混淆手段无法静态拦截；
本 hook 的定位是"代码层挡住一切正常与常规取巧的偷看"，
配合 memory_guard 的运行期记忆清空与运行后日志审计构成纵深防御。

审计：每次拦截（以及所有文件类工具调用）追加写入
$WORKSPACE/debug/.path_guard.log，供运行后人工核对。
"""

import json
import os
import re
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 文件类工具 → 路径字段
FILE_TOOLS = {
    "Read": "file_path",
    "Write": "file_path",
    "Edit": "file_path",
    "NotebookEdit": "notebook_path",
    "NotebookRead": "file_path",
}
WRITE_TOOLS = {"Write", "Edit", "NotebookEdit"}
# Bash 分词分隔符：空白、管道、重定向、命令分隔、引号、括号（吃掉 $(...) 与反引号）
TOKEN_SPLIT = re.compile(r'[\s|&;<>()`\'"\[\]{}]+')


def deny(reason):
    print(f"path_guard: DENIED — {reason}", file=sys.stderr)
    sys.exit(2)


def audit(workspace, tool, target, decision):
    try:
        log_path = os.path.join(workspace, "debug", ".path_guard.log")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {decision} {tool} {target[:300]}\n")
    except OSError:
        pass  # 审计失败绝不阻塞主流程


def normalize(p):
    """展开 ~ 与 $HOME，返回（可能是相对的）路径字符串。"""
    home = os.path.expanduser("~")
    p = p.replace("${HOME}", home).replace("$HOME", home)
    return os.path.expanduser(p)


def main():
    workspace = os.environ.get("WORKSPACE")
    if not workspace:
        sys.exit(0)  # 非 pipeline 会话：放行
    workspace = os.path.realpath(workspace)
    role = os.environ.get("WORKSPACE_ROLE", "agent")

    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # 输入无法解析（harness 变更？）：放行，避免误杀整条流水线

    tool = data.get("tool_name", "")
    tin = data.get("tool_input") or {}
    hook_cwd = os.path.abspath(data.get("cwd") or os.getcwd())

    read_roots = [workspace, os.path.realpath(os.path.join(PROJECT_ROOT, "textbook"))]
    textbook_root = read_roots[1]
    if role == "orchestrator":
        read_roots.append(os.path.realpath(os.path.join(PROJECT_ROOT, "scripts")))
    write_roots = [workspace]

    def inside(path, roots):
        rp = os.path.realpath(path)
        return any(rp == r or rp.startswith(r + os.sep) for r in roots)

    def ok(path, roots):
        """相对路径按 hook cwd 与 workspace 双重解析，任一命中即放行。"""
        path = normalize(path)
        if os.path.isabs(path):
            return inside(path, roots)
        return any(inside(os.path.join(base, path), roots)
                   for base in (hook_cwd, workspace))

    def check(value, roots, target_desc):
        if not ok(value, roots):
            audit(workspace, tool, value, "DENY")
            deny(f"{target_desc} outside workspace: {value}")

    # ---- 结构化文件工具 ----
    if tool in FILE_TOOLS:
        fp = tin.get(FILE_TOOLS[tool], "")
        if not fp:
            audit(workspace, tool, "(missing path)", "DENY")
            deny(f"{tool} without a file path — cannot verify")
        roots = write_roots if tool in WRITE_TOOLS else read_roots
        check(fp, roots, "file path")
        audit(workspace, tool, fp, "ALLOW")
        sys.exit(0)

    if tool in ("Glob", "Grep"):
        path = tin.get("path", "")
        if path:
            check(path, read_roots, "search path")
        audit(workspace, tool, path or "(project)", "ALLOW")
        sys.exit(0)

    # ---- Bash：分词扫描所有疑似路径 ----
    if tool == "Bash":
        cmd = tin.get("command", "")
        tokens = [t for t in TOKEN_SPLIT.split(cmd) if t]
        for tok in tokens:
            base = os.path.basename(tok)
            if base == "claude" or tok.endswith("/claude"):
                audit(workspace, tool, cmd, "DENY")
                deny("launching nested claude sessions is forbidden")
            # 疑似路径：含 /、以 ~ 开头、含 $HOME
            if "/" in tok or tok.startswith("~") or "$HOME" in tok:
                check(tok, read_roots, "path in command")

        # textbook 是**只读**根：上面的分词检查只验证路径可达（读视角），
        # 不区分写方向——`rm -rf textbook/...`、`echo x > textbook/...` 也会通过。
        # 这里补一层写方向检查（启发式，接受少量误杀；混淆手段仍是已知边界）。
        def resolves_into(value, root):
            p = normalize(value)
            cands = [p] if os.path.isabs(p) else [os.path.join(b, p) for b in (hook_cwd, workspace)]
            return any(inside(c, [root]) for c in cands)

        tb_tokens = [t for t in tokens if resolves_into(t, textbook_root)]
        if tb_tokens:
            # 1) 重定向写入：> / >> 之后紧跟的目标解析进 textbook（排除 >&1 之类）
            for m in re.finditer(r"(?<![>&|])>{1,2}(?!&)", cmd):
                rest = cmd[m.end():].lstrip().split(None, 1)
                if rest and resolves_into(rest[0], textbook_root):
                    audit(workspace, tool, cmd, "DENY")
                    deny(f"redirect writes into read-only textbook root: {rest[0]}")
            bases = {os.path.basename(t) for t in tokens}
            # 2) 就地修改/毁灭类命令与 textbook 路径共现
            hit = bases & {"rm", "rmdir", "unlink", "truncate", "chmod", "chown",
                           "touch", "dd", "ln", "mkdir", "tee", "install", "rsync"}
            if hit:
                audit(workspace, tool, cmd, "DENY")
                deny(f"destructive command {sorted(hit)[0]} combined with read-only textbook path")
            # 3) sed -i 就地编辑
            if "sed" in bases and any(t == "--in-place" or t.startswith("-i") for t in tokens):
                audit(workspace, tool, cmd, "DENY")
                deny("sed in-place edit combined with read-only textbook path")
            # 4) cp/mv：最后一个路径参数是目的端——目的端落在 textbook 即写入
            if bases & {"cp", "mv"}:
                path_tokens = [t for t in tokens if "/" in t or t.startswith("~")]
                if path_tokens and resolves_into(path_tokens[-1], textbook_root):
                    audit(workspace, tool, cmd, "DENY")
                    deny(f"cp/mv destination inside read-only textbook root: {path_tokens[-1]}")

        audit(workspace, tool, cmd, "ALLOW")
        sys.exit(0)

    # ---- 其它工具：若带路径字段则检查，否则放行 ----
    fp = tin.get("file_path") or tin.get("notebook_path") or ""
    if fp:
        check(fp, read_roots, "file path")
    sys.exit(0)


if __name__ == "__main__":
    main()
