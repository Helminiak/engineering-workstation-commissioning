#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
lms server status
node scripts/load-commissioning-model.cjs 32768
exec .venv/bin/python scripts/local_agent.py "$@"
