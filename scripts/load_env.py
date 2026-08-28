#!/usr/bin/env python3
"""载入项目根 `.env`（由 setup.sh 写入的 API 配置）。

规则：
- 只读 `PROJECT_ROOT/.env`，逐行解析 `KEY=VALUE`（忽略空行与 # 注释）。
- **已存在的环境变量优先**，.env 不覆盖（用户显式 export 的永远生效）。
- 文件不存在时静默返回——环境变量直接 export 的用户无需 .env。

`.env` 已列入 .gitignore，绝不会被提交。
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()


def load(dotenv_path=None):
    """把 .env 中的键值补进 os.environ（不覆盖已有变量）。"""
    env_file = Path(dotenv_path) if dotenv_path else PROJECT_ROOT / ".env"
    if not env_file.is_file():
        return
    try:
        lines = env_file.read_text(encoding="utf-8").splitlines()
    except OSError:
        return
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


# import 即生效：run.py / spawn.py 只需 `import load_env`
load()
