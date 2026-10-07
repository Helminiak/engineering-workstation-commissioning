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
Integration exit 2 means incomplete. Health checks mandatory local subsystems and CLI authentication; health exit 0 does not prove remote write access or native Bionic behavior.

The reviewed apt batch is already approved, installed and verified; do not repeat it. Run scripts/verify-development.sh and scripts/verify-build-tools.sh for verification. CLI authentication as Helminiak is verified. The private commissioning repository and commissioning/main-work pushes are authorized and verified. Run python3 scripts/verify-github-remote.py after pushes. Other repositories/branches and merge/deploy require separate authorization.
