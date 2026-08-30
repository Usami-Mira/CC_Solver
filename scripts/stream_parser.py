#!/usr/bin/env python3
"""Shared stream-json parser for Claude Code CLI output."""

import json


def parse_stream_event(line):
    """Parse a stream-json event line. Returns (event_type, summary, full_event) tuple.

    event_type: 'init', 'thinking', 'text', 'tool_use', 'tool_result', 'result', 'other'
    summary: human-readable one-liner
    full_event: parsed dict (or None)
    """
    try:
        event = json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return ("other", None, None)

    try:
        return _parse_event(event)
    except Exception:
        # 任何格式化异常（如网关返回 total_cost_usd: null）都不得杀死泵送线程：
        # 泵线程在 result 事件上崩溃会导致"成功的会话被误报为无结果"。
        return ("other", None, event)


def _parse_event(event):
    etype = event.get("type", "")

    if etype == "system" and event.get("subtype") == "init":
        return ("init", f"model={event.get('model')}", event)

    elif etype == "assistant":
        content = event.get("message", {}).get("content", [])
        for block in content:
            bt = block.get("type", "")
            if bt == "thinking":
                t = block.get("thinking", "")
                if t:
                    return ("thinking", t[:300], event)
            elif bt == "text":
                t = block.get("text", "")
                if t:
                    return ("text", t[:500], event)
            elif bt == "tool_use":
                name = block.get("name", "")
                inp = block.get("input", {})
                if name == "Bash":
                    cmd = inp.get("command", "")[:200]
                    return ("tool_use", f"Bash: {cmd}", event)
                elif name in ("Read", "Write", "Edit"):
                    return ("tool_use", f"{name}: {inp.get('file_path', '')}", event)
                else:
                    return ("tool_use", f"{name}", event)

    elif etype == "tool_result":
        content = event.get("content", "")
        if isinstance(content, list):
            content = " ".join(c.get("text", "") if isinstance(c, dict) else str(c) for c in content)
        return ("tool_result", str(content)[:300], event)

    elif etype == "result":
        # 不输出费用（网关价格未知/不可靠）——只报 token 消耗。
        # 网关/代理可能把字段返回为 null —— 逐项强制转 int，
        # 绝不让格式化异常冒泡到泵送线程
        usage = event.get("usage") or {}
        if not isinstance(usage, dict):
            usage = {}

        def _tok(key):
            try:
                return int(usage.get(key) or 0)
            except (TypeError, ValueError):
                return 0

        summary = (f"duration={event.get('duration_ms', 0)}ms "
                   f"turns={event.get('num_turns', 0)} "
                   f"tokens: in={_tok('input_tokens')} out={_tok('output_tokens')} "
                   f"cache_write={_tok('cache_creation_input_tokens')} "
                   f"cache_read={_tok('cache_read_input_tokens')}")
        return ("result", summary, event)

    return ("other", None, event)
