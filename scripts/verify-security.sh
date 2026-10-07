#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
venvs/quant/bin/ruff check scripts/*.py tools/commissioning*.py tools/workbench_mcp.py tests/*.py scripts/engineering-health-check --output-format json > evidence/ruff-final.json
venvs/quant/bin/mypy --follow-imports skip tools/commissioning_mbo.py tools/commissioning_forensics.py tools/commissioning_rag.py > evidence/mypy.txt
python3 scripts/secret_scan.py
uv pip check --python .venv/bin/python
uv pip check --python venvs/quant/bin/python
uv pip check --python venvs/gpu/bin/python
python3 - <<'PY'
import json
from pathlib import Path
for name in ['quant','local-agent']:
 obj=json.loads(Path(f'evidence/{name}-audit.json').read_text())
 assert 'dependencies' in obj
 assert all(not d.get('vulns') for d in obj['dependencies']), name
obj=json.loads(Path('evidence/npm-audit.json').read_text());assert obj['metadata']['vulnerabilities']['total']==0
assert json.loads(Path('evidence/ruff-final.json').read_text())==[]
print('PASS: recorded dependency audits, lint, scoped type checks, compatibility, staged secret heuristics')
PY
