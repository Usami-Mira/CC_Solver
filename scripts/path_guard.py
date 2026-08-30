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
三类豁免（防误杀）：/dev/null 等设备文件白名单放行；磁盘上不存在的路径
不可能泄漏数据，放行——但重定向目标（>/>>）是写入方向，不在此列；
裸 "/"（内联代码除号）放行——除非它跟在 ls/find/grep 等命令后当路径
参数用（`ls /`、`find / -name ...` 从根扫描文件系统，仍拦截）。

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
# 设备文件白名单：/dev/null 之类的重定向目标是 UNIX 惯例，不是数据通道
DEVICE_PATH_OK = re.compile(r'^/dev/(null|zero|random|urandom|full|stdin|stdout|stderr|tty.*|pts/.*|fd/.*)$')
# 重定向写入目标（> / >>）：写入方向，即使目标尚不存在也必须检查
REDIRECT_WRITE_RE = re.compile(r'(?<![>&|])>{1,2}(?!&)\s*([^\s|&;<>]+)')
# 以路径为参数的文件操作命令：裸 "/" 紧跟在这些命令之后（如 `ls /`、
# `find / -name ...`）= 从文件系统根部扫描，必须拦截；其余场景的裸 "/"
# 几乎全是内联代码里的除号（python -c "a / b" 被分词成 a、/、b）
ROOT_ARG_CMDS = {"ls", "find", "cat", "head", "tail", "less", "more",
                 "grep", "rg", "rm", "cp", "mv", "du", "tree", "stat",
                 "tar", "rsync", "diff", "wc", "file", "truncate",
                 "chmod", "chown", "touch", "dd"}
CMD_SEGMENT_RE = re.compile(r";|&&|\|\||\|")


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
        # 重定向目标（>/>>）是写入方向：即使尚不存在也必须全程检查
        redirect_targets = {m.group(1) for m in REDIRECT_WRITE_RE.finditer(cmd)}

        # 裸 "/" 是否作为路径参数出现：逐命令段（; && || | 切分）判断——
        # 段首是文件操作命令且段内含孤立 "/"（两侧是空白）才算。
        # 这样 `ls /`、`grep -r x /` 被拦，而 `ls ws && python3 -c "a / b"`
        # 里的除号不受牵连。
        def _segment_scans_root(seg):
            words = [w for w in seg.split() if not w.startswith("-")]
            return (bool(words) and os.path.basename(words[0]) in ROOT_ARG_CMDS
                    and re.search(r"(^|\s)/(\s|$)", seg) is not None)

        root_arg_segments = any(_segment_scans_root(seg)
                                for seg in CMD_SEGMENT_RE.split(cmd))

        for tok in tokens:
            base = os.path.basename(tok)
            if base == "claude" or tok.endswith("/claude"):
                audit(workspace, tool, cmd, "DENY")
                deny("launching nested claude sessions is forbidden")
            # 疑似路径：含 /、以 ~ 开头、含 $HOME
            if "/" in tok or tok.startswith("~") or "$HOME" in tok:
                norm = normalize(tok)
                if DEVICE_PATH_OK.match(norm):
                    continue  # /dev/null 等设备文件：放行（历史误杀修复）
                if norm.rstrip("/") == "" and not root_arg_segments:
                    # 裸 "/"（含 "//"）：内联代码里的除号——a / b 分词后
                    # a、/、b，"/" 自己不指向任何数据。仅当整条命令里存在
                    # `文件操作命令 … / …` 段（上面已判定）时才当路径拦。
                    continue
                if tok not in redirect_targets and norm not in redirect_targets:
                    # 磁盘上不存在的路径不可能泄漏数据——放行。这消除了物理符号
                    # （\Gamma、\sin^2 等出现在命令里被误判为路径）的误杀。
                    cands = [norm] if os.path.isabs(norm) else \
                        [os.path.join(b, norm) for b in (hook_cwd, workspace)]
                    if not any(os.path.exists(c) for c in cands):
                        continue
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
