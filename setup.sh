#!/bin/bash
# CC_Solver project setup script
# Sets up all dependencies and environments

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== CC_Solver Project Setup ==="
echo "Working directory: $SCRIPT_DIR"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Setup RAG environment
echo ""
echo "=== Setting up RAG Environment ==="
RAG_DIR="textbook"
RAG_VENV="$RAG_DIR/rag_env"

if [ ! -d "$RAG_VENV" ]; then
    echo "Creating RAG virtual environment..."
    python3 -m venv "$RAG_VENV"
    echo "RAG venv created at $RAG_VENV"
else
    echo "RAG venv already exists at $RAG_VENV"
fi

echo "Installing RAG dependencies..."
"$RAG_VENV/bin/pip" install --upgrade pip --quiet
"$RAG_VENV/bin/pip" install --quiet \
    torch \
    FlagEmbedding \
    sentence-transformers \
    weaviate-client \
    transformers \
    numpy \
    scipy \
    mpmath \
    sympy \
    matplotlib

echo "RAG environment ready."

# Test RAG
echo ""
echo "=== Testing RAG System ==="
if "$RAG_VENV/bin/python" "$RAG_DIR/rag_build/query_rag.py" "test query" >/dev/null 2>&1; then
    echo "✓ RAG system working"
else
    echo "⚠ RAG system may need Weaviate running"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To use RAG in your code:"
echo "  textbook/rag_env/bin/python textbook/rag_build/query_rag.py \"your query\""
echo ""
