#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
lms server start --bind 127.0.0.1 --port 1234
node scripts/load-commissioning-model.cjs 32768
exec .venv/bin/python scripts/local_agent.py "$@"
