#!/usr/bin/env python3
"""Hook to ensure file operations are within workspace directory.

Only active when WORKSPACE environment variable is set (i.e., in sub-agents).
Skips check for main Claude session (no WORKSPACE env var).
"""
import sys
import json
import os

# 检查是否有 WORKSPACE 环境变量（只有 sub-agent 才有）
workspace = os.environ.get("WORKSPACE")
if not workspace:
    # 没有 WORKSPACE，说明是主 Claude 会话，跳过检查
    sys.exit(0)

# 读取 hook 输入（包含工具调用信息）
hook_input = json.load(sys.stdin)

# 获取文件路径
tool_name = hook_input.get("tool_name", "")
tool_input = hook_input.get("tool_input", {})
file_path = tool_input.get("file_path", "")

if not file_path:
    # 没有文件路径，允许操作
    sys.exit(0)

# 转换为绝对路径
file_path_abs = os.path.abspath(file_path)
workspace_abs = os.path.abspath(workspace)

# 检查文件是否在 workspace 内
if not file_path_abs.startswith(workspace_abs + os.sep) and file_path_abs != workspace_abs:
    print(f"Error: File operation outside workspace!", file=sys.stderr)
    print(f"  File: {file_path_abs}", file=sys.stderr)
    print(f"  Workspace: {workspace_abs}", file=sys.stderr)
    sys.exit(1)

# 允许操作
sys.exit(0)
