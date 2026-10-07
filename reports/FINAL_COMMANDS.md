# Resume and verification commands
```bash
cd /home/joe/LLM-Workspace
scripts/show_status.sh
scripts/engineering-health-check --json evidence/health-current.json
scripts/start-local-agent.sh tests/local-agent-task.txt --transcript state/new-agent-task.json
.venv/bin/python tests/local_llm_acceptance.py
python3 tests/end_to_end.py
scripts/verify-before-commit.sh
git log -1
```
Current integration/health exit 2 means incomplete. Do not treat as success.

The reviewed apt batch is already approved, installed and verified; do not repeat it. Run scripts/verify-development.sh and scripts/verify-build-tools.sh for verification. Operator runs gh auth login. Creating a new private repository requires separate authorization. No automatic merge/deploy/push.
