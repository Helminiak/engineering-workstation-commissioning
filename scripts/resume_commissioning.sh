#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
python3 scripts/commission.py status
python3 - <<'PY'
import json
p=json.load(open('commissioning/progress.json'))
for k,v in p['stages'].items():
 if v['status'] not in ('PASS','PASS_WITH_LIMITATIONS'):
  print('Next unfinished stage:',k);print('Read commissioning/NEXT_AGENT.md and recorded verifier evidence before executing.');break
PY
