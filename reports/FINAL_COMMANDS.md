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

After operator approval only: scripts/development-install-request.sh --operator-approved; then scripts/verify-development.sh. Operator runs gh auth login. Creating a new private repository requires separate authorization. No automatic merge/deploy/push.
