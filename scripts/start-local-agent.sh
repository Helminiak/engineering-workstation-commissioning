#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
# Preserve the operator's app, quantization, context, slots and security settings.
# Explicit model loading is a separate reviewed action, never a resume side effect.
node scripts/model-info.cjs | python3 -c '
import json,sys
models=json.load(sys.stdin)
if not any(m.get("identifier")=="qwen/qwen3.8-27b" for m in models):
 sys.exit("Required local Qwen model is not loaded. Select/load the intended model in your app; no automatic reload attempted.")
'
exec .venv/bin/python scripts/local_agent.py "$@"
