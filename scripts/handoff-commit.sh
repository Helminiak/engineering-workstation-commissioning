#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
python3 scripts/commission.py checkpoint "${1:?Supply checkpoint message}"
# Explicit source/state paths only. Never add raw logs or entire workspace.
git add commissioning scripts tests handoff reports configs tools/workbench_mcp.py tools/commissioning*.py
scripts/verify-before-commit.sh
git diff --cached --stat
git commit -m "$1"
# No automatic push until an authorized private remote exists.
