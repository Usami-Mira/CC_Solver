#!/usr/bin/env python3
"""Claude Code 状态栏：实时显示 CC_Solver pipeline 进度。

Claude Code 定期调用本脚本，从 stdin 传入会话信息（JSON），
脚本输出一行文本，显示在界面底部。

显示内容：最近活跃的 problem workspace 的 pipeline 状态（读取 .state）。
设计原则：快（只读几个小文件）、永不报错（任何异常都降级为简短输出）。
"""

import sys
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"

VERDICT_ICON = {"PASS": "✅", "FAIL": "❌", "REVISE": "🔁", "SOUND": "🔍",
                "CONSENSUS": "🤝", "DISPUTED": "⚔️"}
GREEN = "\033[32m"
DIM = "\033[90m"
CYAN = "\033[36m"
RESET = "\033[0m"


def parse_state(text):
    """解析 .state：支持三种格式——
    1. 'key: value' 多行格式（新协议：pipeline/stage/iteration/...）
    2. 单单词格式（如 'planner'）
    3. 多行阶段列表（旧格式，最后一行视为当前阶段）
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    kv_lines = [ln for ln in lines if ":" in ln]
    if kv_lines:
        d = {}
        for ln in kv_lines:
            k, v = ln.split(":", 1)
            d[k.strip()] = v.strip()
        return d
    if lines:
        return {"stage": lines[-1]}
    return {}


def fmt_age(seconds):
    """把秒数格式化为 3m / 2h13m / 5d 之类的短格式。"""
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        h, m = divmod(seconds // 60, 60)
        return f"{h}h{m:02d}m" if m else f"{h}h"
    return f"{seconds // 86400}d"


def find_latest_state():
    """新布局：{ws}/debug/.state；旧布局：{ws}/.state。取最近修改的一个。"""
    if not PROBLEMS_DIR.is_dir():
        return None
    candidates = [p for p in PROBLEMS_DIR.glob("*/debug/.state") if p.is_file()]
    candidates += [p for p in PROBLEMS_DIR.glob("*/.state") if p.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def latest_progress(base_dir):
    """读最近的 .* .progress（Agent 内部进度），返回一行文本或 ""。"""
    try:
        cands = [p for p in base_dir.glob(".*.progress") if p.is_file()]
        if not cands:
            return ""
        p = max(cands, key=lambda q: q.stat().st_mtime)
        txt = p.read_text(encoding="utf-8", errors="replace").strip()
        if not txt:
            return ""
        role = p.name[1:-len(".progress")]
        return f"{role} {txt.splitlines()[-1][:40]}"
    except Exception:
        return ""


def main():
    try:
        info = json.load(sys.stdin)
    except Exception:
        info = {}
    model = ""
    try:
        model = (info.get("model") or {}).get("display_name", "")
    except Exception:
        pass

    state_path = find_latest_state()
    if state_path is None:
        print(f"⚛ CC_Solver · 暂无 pipeline 记录{(' · ' + model) if model else ''}")
        return

    try:
        state = parse_state(state_path.read_text(encoding="utf-8", errors="replace"))
        # 新布局下 .state 在 {ws}/debug/ 里；日志/进度文件与 .state 同目录
        base_dir = state_path.parent
        ws_name = base_dir.parent.name if base_dir.name == "debug" else base_dir.name
        age = time.time() - state_path.stat().st_mtime

        # 判断是否正在运行：工作区内任一 .*.log 在 120 秒内有更新。
        # 注意不能只看 .orchestrator.log —— sub-Agent 工作期间
        # Orchestrator 阻塞在 spawn.py 里，主日志不会更新，
        # 而 .{Role}.log 由 spawn.py 的 pump 线程实时写入。
        logs = [p for p in state_path.parent.glob(".*.log") if p.is_file()]
        running_log = None
        now = time.time()
        for p in logs:
            if now - p.stat().st_mtime < 120:
                if running_log is None or p.stat().st_mtime > running_log.stat().st_mtime:
                    running_log = p

        running = running_log is not None
        active_role = ""
        if running:
            active_role = running_log.name[1:-4]  # '.Builder.log' -> 'Builder'
            if active_role == "orchestrator":
                active_role = "Orchestrator"

        pipeline = state.get("pipeline", "?")
        stage = state.get("stage")
        iteration = state.get("iteration")
        verdict = state.get("last_verdict")
        nxt = state.get("next")

        dot = f"{GREEN}▶{RESET}" if running else f"{DIM}⏸{RESET}"
        parts = [f"⚛ {dot} {CYAN}{pipeline}{RESET} · {ws_name}"]
        if stage:
            s = stage
            if iteration:
                s += f" {iteration}"
            parts.append(s)
        if running and active_role:
            parts.append(f"{active_role} 运行中")
        if running:
            prog = latest_progress(base_dir)
            if prog:
                parts.append(prog)
        if verdict and verdict not in ("-", ""):
            parts.append(f"{VERDICT_ICON.get(verdict, '·')} {verdict}")
        if nxt:
            parts.append(f"→ {nxt}")
        if not running:
            parts.append(f"{DIM}更新于 {fmt_age(age)} 前{RESET}")
        print(" | ".join(parts))
    except Exception:
        # 任何异常都降级为简短输出，绝不阻塞状态栏
        print("⚛ CC_Solver")


if __name__ == "__main__":
    main()
