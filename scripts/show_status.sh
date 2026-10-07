#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
exec python3 scripts/commission.py status
