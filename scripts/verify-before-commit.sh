#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
git diff --check
git diff --cached --check
python3 scripts/secret_scan.py
python3 tests/test_runner.py
.venv/bin/python tests/test_bridge.py
