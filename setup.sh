#!/bin/bash
# CC_Solver 一键配置：依赖安装 + 防偷看机制自检 + 回归测试
#
# 用法:
#   bash setup.sh            # 完整配置（含 pip 安装，首次较慢）
#   bash setup.sh --quick    # 跳过 pip 安装与 RAG 测试（验证配置用）
#
# 幂等：重复运行安全。

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

# ---------- [1/6] 先决条件 ----------
echo ""
echo "=== [1/6] 先决条件 ==="
if command -v python3 >/dev/null; then
    ok "python3 $(python3 --version 2>&1 | awk '{print $2}')"
else
    bad "未找到 python3"
fi
if command -v git >/dev/null; then
    ok "git $(git --version | awk '{print $3}')"
else
    bad "未找到 git"
fi
if command -v claude >/dev/null; then
    ok "claude CLI: $(claude --version 2>/dev/null | head -1)"
else
    warn "未找到 claude CLI（pipeline 运行需要；交互式使用请安装 Claude Code）"
fi

# ---------- [2/6] RAG 虚拟环境 ----------
echo ""
echo "=== [2/6] RAG 环境 ==="
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

# ---------- [3/6] path_guard（防偷看硬封锁）自检 ----------
echo ""
echo "=== [3/6] path_guard 自检 ==="
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

# ---------- [4/6] memory_guard（记忆防火墙）状态 ----------
echo ""
echo "=== [4/6] memory_guard ==="
if python3 scripts/memory_guard.py status; then
    ok "记忆目录状态见上（首次运行时自动 git 化）"
else
    warn "memory_guard status 异常（不影响安装）"
fi

# ---------- [5/6] 回归测试 ----------
echo ""
echo "=== [5/6] 回归测试 ==="
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

# ---------- [6/6] 总结 ----------
echo ""
echo "=== 完成 ==="
if [ "$FAILURES" = "0" ]; then
    echo "  全部就绪。运行题目: python3 scripts/run.py problems/<workspace>"
else
    echo "  有 $FAILURES 项失败，请按上方 ✗ 提示排查。"
fi
exit "$FAILURES"
