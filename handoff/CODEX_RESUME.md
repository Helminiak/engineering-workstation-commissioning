# Reboot resume checkpoint

Checkpoint captured 2026-10-07T02:12:32.168563+00:00. Operator requested saving work and stopping new tasks. No reboot, shutdown, service stop, configuration restore, install, model reload, or new commissioning phase was initiated. No commissioning stage is IN_PROGRESS. Existing services remain running until the operator reboots. Resume only after the operator returns.

## Verified state and current failure

Historical native Bionic acceptance remains PASS, independently verified from persisted native tool-call/result records: 11 shell commands, native file write/read, Bash, Python385, pytest2tests and scoped Git status/diff. Do not rerun or overwrite the fixture. Proof: reports/BIONIC_NATIVE_ACCEPTANCE.json; full owner-only trace: evidence/bionic-native-historical-trace.json.

Current Bionic usability is BLOCKED. Actual operator-loaded Qwen Q4_K_M has105472-token context, four parallel slots and full GPU offload. A hello turn at21:59:15 local produced122973 tokens, exceeding capacity by17501. Static base system text tokenizes474, stored message text167; the large dynamic payload is not attributed to a specific connector. Regular LM Studio CLI hello succeeds with36 prompt tokens, plain API control with13. Pristine Bionic-versus-regular GUI comparison remains unverified; Codex has no desktop UI controls. Read reports/BIONIC_CONTEXT_DIAGNOSIS.md and .json.

Pre-reboot GPU snapshot: total32607MiB, used28228MiB, free3880MiB. Earlier diagnosis baseline free3421MiB; readings vary. No context increase or app/plugin/security configuration change was made during this diagnosis. Do not infer current Q4/four-slot feasibility from the historical Q6/32K benchmarks.

## Preserved configuration and evidence

Configuration backup directory: `/home/joe/LLM-Workspace/backups/bionic-context-20261007T015809Z`
Manifest with original destinations and SHA-256: `/home/joe/LLM-Workspace/backups/bionic-context-20261007T015809Z/manifest.json`
12 source files were copied; directory0700 and backup files0600. Settings/model data/backend preferences/MCP/project registry are included; credential values were not printed or committed. Read the manifest locally. Do not restore blindly or upload these backups.

Fresh pre-reboot processes/listeners/model snapshot: `/home/joe/LLM-Workspace/state/reboot_snapshot.json`.
Current exact commit and remote verification: `/home/joe/LLM-Workspace/state/latest_checkpoint.json` and `/home/joe/LLM-Workspace/evidence/github-remote-verification.json`.
Raw logs remain local: `/home/joe/LLM-Workspace/evidence/bionic-context-log-excerpts.json`, `/home/joe/LLM-Workspace/logs/bionic-native-launch.log`, `/home/joe/.lmstudio/apps/bionic/server-logs/2026-10/2026-10-06.1.log` and `/home/joe/.config/Bionic/logs/main.log`. Read only targeted excerpts; do not dump requests/credentials.

## Running at checkpoint

- Bionic mainPID859204 and helperPIDs859217,859218,859221,859315,859318,860575. Main process owns loopback SDK port41343 and authenticated API1234. LM Studio desktop was not running.
- llama-server PID866715, loopback44293, model IDLE in lms ps.
- Local Workbench stdio MCP pythonPID859574 (workbench_mcp.py), attached to Bionic.
- Python monitorPID289483 (monitor.py), loopback8765; unrelated PythonPID232059 purpose not verified. Both left untouched.
- Codex/session processes listed in state/reboot_snapshot.json; current primaryPID622903 owns loopback44273. Other system loopback listeners include CUPS631 and DNS. No external-facing service was exposed by commissioning.
- No active commissioning installation, benchmark, model generation or stage runner at capture. PIDs/ports are historical and will change after reboot. Transient checkpoint Python process in raw snapshot exits before handoff.

## Exact next checks after reboot

First command: `cd /home/joe/LLM-Workspace && scripts/show_status.sh`.

```bash
cd /home/joe/LLM-Workspace
whoami
pwd
uname -r
nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used,memory.free --format=csv,noheader
free -h
lms ps
lms server status
ps -eo pid,comm
ss -ltnp
git status --short
git log -1 --format='%H %s'
python3 scripts/verify-github-remote.py
```

Read the backup manifest and diagnostic timestamps before acting. After reboot no model/API may be loaded; record this as NOT_TESTED/incomplete until the operator chooses an app/model. Do not start both apps blindly: a previous Bionic launch unloaded the commissioned model. Do not run scripts/start-local-agent.sh as an automatic resume step because it requests Q6/32K, differing from the saved Q4/105472/four-slot settings.

Once the intended local app/model is available, read its *actual* load configuration and measure VRAM again. Then:
```bash
scripts/engineering-health-check --json evidence/health-after-reboot.json
lms chat qwen/qwen3.8-27b --prompt hello --stats --reasoning off --dont-fetch-catalog
python3 scripts/verify-bionic-history.py
```

Keep CLI/Codex controls separate from Bionic-native results. Operator should compare hello in pristine native Bionic and regular LM Studio GUI chats on the SAME local model, without attachments/settings changes; record timestamps and correlate fresh server counts. Inspect enabled tool/schema/instruction payload by project/provider. Existing inspect-bionic-context.py uses dated incident snapshots/logs; update its inputs and log date before treating it as a new post-reboot observation. Do not enlarge context or disable integrations based only on old data. Historical acceptance PASS stays intact while current usability remains BLOCKED until a fresh native retest succeeds.

## Git, authorization and prohibited actions

Private repository: https://github.com/Helminiak/engineering-workstation-commissioning
Only approved branch: commissioning/main-work. Read AUTHORIZATION.json. Normal workspace work and this private task-branch push are authorized. Other repositories/branches, drivers/kernel/firmware, deleting existing data, security controls, network exposure, merge or deployment need approval. Never print credentials, merge, or force-push. Read local HEAD and remote verification for the exact checkpoint commit rather than assuming a hash embedded before commit is current.
