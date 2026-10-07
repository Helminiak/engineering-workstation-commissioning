# Architecture
Codex commissions and repairs; local Qwen performs scoped engineering via Local Workbench; ChatGPT reviews architecture using sanitized handoff files. Persistent stage state and append-only command evidence underpin restart. Local services bind loopback. Execution is normal-user code execution, not an OS sandbox. Optional documentation tools must remain independent of core execution.

## Actual execution paths
scripts/local_agent.py uses the loopback authenticated OpenAI-compatible API and an independent stdio core MCP session. Optional connectors are excluded. Bionic native Connected Apps remains configured but its UI and approval mode are not verified.

scripts/commission.py persists stage start/end, command, exit status, stdout/stderr evidence, outcomes and issues. It updates handoffs and status; interrupted tool actions require reconciliation, not blind replay. transcripts in state/ and command audits in logs/local-agent/ are local and excluded from Git.

Environments: .venv retains original local-agent tools; venvs/quant is Python 3.12 scientific/tooling; venvs/gpu is Python 3.12 with CUDA 13.0 PyTorch. Lock manifests are in configs/. Existing legacy startup helper still requests 64K; use scripts/start-local-agent.sh for commissioned 32K instead.
