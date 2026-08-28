#!/bin/bash
# CC_Solver 一键配置：先决条件 + git 身份 + Claude CLI + API key + 依赖 + 防偷看自检 + 回归测试
#
# 用法:
#   bash setup.sh            # 完整配置（含 pip 安装，首次较慢）
#   bash setup.sh --quick    # 跳过 pip 安装与 RAG 测试（验证配置用）
#
# 幂等：重复运行安全。所有交互提示都可用环境变量预先提供：
#   GIT_NAME / GIT_EMAIL / ANTHROPIC_AUTH_TOKEN / ANTHROPIC_API_KEY / ANTHROPIC_BASE_URL

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

QUICK=0
[ "$1" = "--quick" ] && QUICK=1

FAILURES=0
ok()   { echo "  ✓ $1"; }
warn() { echo "  ⚠ $1"; }
bad()  { echo "  ✗ $1"; FAILURES=$((FAILURES + 1)); }

echo "=== CC_Solver Project Setup ==="
echo "Project root: $SCRIPT_DIR"

# ---------- [1/8] 先决条件 ----------
echo ""
echo "=== [1/8] 先决条件 ==="
if command -v python3 >/dev/null; then
    ok "python3 $(python3 --version 2>&1 | awk '{print $2}')"
else
    bad "未找到 python3"
fi
if command -v git >/dev/null; then
    ok "git $(git --version | awk '{print $3}')"
else
    bad "未找到 git（Ubuntu: sudo apt-get install git / macOS: brew install git）"
fi
if command -v claude >/dev/null; then
    ok "claude CLI: $(claude --version 2>/dev/null | head -1)"
else
    echo "  未找到 claude CLI，尝试自动安装..."
    if command -v npm >/dev/null; then
        if npm install -g @anthropic-ai/claude-code >/dev/null 2>&1 && command -v claude >/dev/null; then
            ok "claude CLI 已安装: $(claude --version 2>/dev/null | head -1)"
        else
            bad "claude CLI 自动安装失败（权限不足可试: sudo npm install -g @anthropic-ai/claude-code，或先装 Node.js ≥18）"
        fi
    else
        bad "未找到 claude CLI 且无 npm——先安装 Node.js ≥18，再运行 npm install -g @anthropic-ai/claude-code"
    fi
fi

# ---------- [2/8] Git 身份（缺了每次提交都会告警） ----------
echo ""
echo "=== [2/8] Git 身份 ==="
if ! command -v git >/dev/null; then
    bad "git 缺失，跳过身份配置"
else
    CFG_NAME="$(git config user.name 2>/dev/null)"
    CFG_EMAIL="$(git config user.email 2>/dev/null)"
    if [ -n "$CFG_NAME" ] && [ -n "$CFG_EMAIL" ]; then
        ok "git 身份已配置: $CFG_NAME <$CFG_EMAIL>"
    else
        # 交互提示；非交互时用 SETUP_GIT_NAME/SETUP_GIT_EMAIL 或系统用户名兜底
        NEW_NAME="$SETUP_GIT_NAME"
        NEW_EMAIL="$SETUP_GIT_EMAIL"
        if [ -t 0 ]; then
            [ -z "$NEW_NAME" ] && read -r -p "  git user.name  [默认: ${SETUP_GIT_NAME:-$USER}]: " NEW_NAME
            [ -z "$NEW_EMAIL" ] && read -r -p "  git user.email [默认: ${SETUP_GIT_EMAIL:-$USER@$(hostname)}]: " NEW_EMAIL
        fi
        NEW_NAME="${NEW_NAME:-$USER}"
        NEW_EMAIL="${NEW_EMAIL:-$USER@$(hostname)}"
        if git config --global user.name "$NEW_NAME" && git config --global user.email "$NEW_EMAIL"; then
            ok "已设置全局 git 身份: $NEW_NAME <$NEW_EMAIL>"
        else
            bad "git 身份设置失败（可手动: git config --global user.name \"你的名字\"）"
        fi
    fi
fi

# ---------- [3/8] API 配置（Claude CLI 的模型接入） ----------
echo ""
echo "=== [3/8] API 配置 ==="
ENV_FILE="$SCRIPT_DIR/.env"
# .env 已含密钥则直接用（脚本运行时由 scripts/load_env.py 自动载入）
if [ -f "$ENV_FILE" ] && grep -qE "^(ANTHROPIC_AUTH_TOKEN|ANTHROPIC_API_KEY)=" "$ENV_FILE" 2>/dev/null; then
    ok ".env 已配置 API key（$(grep -cE '^ANTHROPIC_' "$ENV_FILE") 个 ANTHROPIC_* 变量，scripts/load_env.py 自动载入）"
elif [ -n "$ANTHROPIC_AUTH_TOKEN" ] || [ -n "$ANTHROPIC_API_KEY" ]; then
    # 环境变量里已有（当前 shell / 启动器导出）——持久化到 .env，
    # 使任何新 shell 直接运行 pipeline 也能工作（.env 已入 .gitignore，不会被提交）
    {
        echo "# CC_Solver API 配置 — 由 setup.sh 生成，切勿提交"
        [ -n "$ANTHROPIC_AUTH_TOKEN" ] && echo "ANTHROPIC_AUTH_TOKEN=$ANTHROPIC_AUTH_TOKEN"
        [ -n "$ANTHROPIC_API_KEY" ] && echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY"
        [ -n "$ANTHROPIC_BASE_URL" ] && echo "ANTHROPIC_BASE_URL=$ANTHROPIC_BASE_URL"
        [ -n "$ANTHROPIC_MODEL" ] && echo "ANTHROPIC_MODEL=$ANTHROPIC_MODEL"
    } > "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    ok "已从环境变量持久化 API 配置到 .env（权限 600，已入 .gitignore）"
else
    # 什么都没有：交互式询问
    if [ -t 0 ]; then
        echo "  未检测到 API 配置。按量计费/第三方网关（如硅基流动）需要："
        echo "    ANTHROPIC_AUTH_TOKEN（或 ANTHROPIC_API_KEY）+ ANTHROPIC_BASE_URL"
        read -r -s -p "  API key/token（输入隐藏，回车跳过则稍后手动配置）: " INPUT_TOKEN; echo ""
        if [ -n "$INPUT_TOKEN" ]; then
            read -r -p "  Base URL（第三方网关填对应地址，官方 API 直接回车）: " INPUT_URL
            {
                echo "# CC_Solver API 配置 — 由 setup.sh 生成，切勿提交"
                if [ -n "$INPUT_URL" ]; then
                    echo "ANTHROPIC_AUTH_TOKEN=$INPUT_TOKEN"
                    echo "ANTHROPIC_BASE_URL=$INPUT_URL"
                else
                    echo "ANTHROPIC_API_KEY=$INPUT_TOKEN"
                fi
            } > "$ENV_FILE"
            chmod 600 "$ENV_FILE"
            ok "API 配置已写入 .env（权限 600，已入 .gitignore）"
        else
            bad "未配置 API key——可稍后重跑 bash setup.sh，或手动 export ANTHROPIC_AUTH_TOKEN / ANTHROPIC_BASE_URL"
        fi
    else
        bad "非交互环境且未检测到 API 配置——请 export ANTHROPIC_AUTH_TOKEN 与 ANTHROPIC_BASE_URL 后重跑，或手动创建 .env"
    fi
fi
# .env 存在时确认它不会被提交
if [ -f "$ENV_FILE" ]; then
    if git check-ignore -q "$ENV_FILE" 2>/dev/null; then
        ok ".env 已被 .gitignore 排除（不会提交密钥）"
    else
        bad ".env 未被 git 忽略——请确认 .gitignore 含 .env 条目！"
    fi
fi

# ---------- [4/8] RAG 虚拟环境 ----------
echo ""
echo "=== [4/8] RAG 环境 ==="
RAG_DIR="textbook"
RAG_VENV="$RAG_DIR/rag_env"

if [ ! -d "$RAG_VENV" ]; then
    echo "  创建 RAG 虚拟环境..."
    python3 -m venv "$RAG_VENV" && ok "venv: $RAG_VENV" || bad "venv 创建失败"
else
    ok "venv 已存在: $RAG_VENV"
fi

if [ "$QUICK" = "1" ]; then
    warn "--quick：跳过 pip 安装与 RAG 测试"
else
    echo "  安装 RAG 依赖（首次可能较慢）..."
    if "$RAG_VENV/bin/pip" install --upgrade pip --quiet && \
       "$RAG_VENV/bin/pip" install --quiet \
           torch FlagEmbedding sentence-transformers weaviate-client \
           transformers numpy scipy mpmath sympy matplotlib; then
        ok "依赖安装完成"
    else
        bad "pip 安装失败（国内网络可试: pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple）"
    fi

    if "$RAG_VENV/bin/python" "$RAG_DIR/rag_build/query_rag.py" "test query" >/dev/null 2>&1; then
        ok "RAG 查询可用"
    else
        warn "RAG 查询失败（模型/向量库缺失，或 Weaviate 未启动）"
    fi
fi

# ---------- [5/8] path_guard（防偷看硬封锁）自检 ----------
echo ""
echo "=== [5/8] path_guard 自检 ==="
if [ ! -f scripts/path_guard.py ]; then
    bad "scripts/path_guard.py 缺失"
elif [ ! -f .claude/settings.json ]; then
    bad ".claude/settings.json 缺失（hook 未注册）"
else
    # 工作区外访问必须被 exit(2) 硬拦截
    WS_TMP="$(mktemp -d)"
    mkdir -p "$WS_TMP/debug"
    printf '{"tool_name":"Read","tool_input":{"file_path":"/etc/passwd"}}' | \
        WORKSPACE="$WS_TMP" python3 scripts/path_guard.py >/dev/null 2>&1
    rc=$?
    if [ "$rc" = "2" ]; then
        ok "工作区外访问被硬拦截 (exit 2)"
    else
        bad "工作区外访问未拦截 (exit $rc)"
    fi
    # 工作区内访问必须放行
    touch "$WS_TMP/problem.md"
    printf '{"tool_name":"Read","tool_input":{"file_path":"%s/problem.md"}}' "$WS_TMP" | \
        WORKSPACE="$WS_TMP" python3 scripts/path_guard.py >/dev/null 2>&1 \
        && ok "工作区内访问放行" || bad "工作区内访问被误拦"
    # 未设 WORKSPACE（交互式会话）必须直通
    printf '{"tool_name":"Read","tool_input":{"file_path":"/etc/passwd"}}' | \
        python3 scripts/path_guard.py >/dev/null 2>&1 \
        && ok "非 pipeline 会话不受影响" || bad "无 WORKSPACE 时误拦"
    rm -rf "$WS_TMP"
fi

# ---------- [6/8] memory_guard（记忆防火墙）状态 ----------
echo ""
echo "=== [6/8] memory_guard ==="
if python3 scripts/memory_guard.py status; then
    ok "记忆目录状态见上（首次运行时自动 git 化）"
else
    warn "memory_guard status 异常（不影响安装）"
fi

# ---------- [7/8] 回归测试 ----------
echo ""
echo "=== [7/8] 回归测试 ==="
if python3 scripts/test_git_integration.py 2>&1 | grep -qE "^OK"; then
    ok "git 集成测试通过"
else
    bad "git 集成测试失败（详见: python3 scripts/test_git_integration.py）"
fi
if python3 scripts/test_path_guard.py 2>&1 | grep -q "PASSED"; then
    ok "path_guard 测试通过"
else
    bad "path_guard 测试失败（详见: python3 scripts/test_path_guard.py）"
fi

# ---------- [8/8] 总结 ----------
echo ""
echo "=== 完成 ==="
if [ "$FAILURES" = "0" ]; then
    echo "  全部就绪。运行题目: python3 scripts/run.py problems/<workspace>"
else
    echo "  有 $FAILURES 项失败，请按上方 ✗ 提示排查。"
fi
exit "$FAILURES"
