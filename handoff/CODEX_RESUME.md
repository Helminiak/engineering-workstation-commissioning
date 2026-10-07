# Codex restart guide

Read `handoff/MASTER_HANDOFF.md`, `handoff/STATUS.md`, `handoff/progress.json`, `handoff/CHECKPOINT.json`, then `commissioning/AUTHORIZATION.json`. Do not depend on conversation history. Operator stopped new work for urgent usage checkpoint; no stage/agent process remains active. This instruction supersedes the earlier autonomous-run instruction until a new resume request.

On authorized resume:

```bash
cd /home/joe/LLM-Workspace
scripts/show_status.sh
git status --short
git log -5 --format='%H %s'
python3 scripts/capture-checkpoint-state.py
python3 scripts/verify-github-remote.py
```

Read-only host diagnostics may require escalation under the managed sandbox. Do not treat sandbox-hidden GPU/API/process state as a host outage. Do not change drivers or security settings to overcome sandbox restrictions.

Reconcile local LLM work before writing: compare currentHEAD and remote with CHECKPOINT.json; a receipt-only commit may follow the recorded content checkpoint; inspect gitdiff, commissioning/progress.json, NEW evidence files, state transcripts and logs/local-agent. Identify claimedPASS versus independently verified exit/artifact proof. Preserve local LLM files and logs; never reset/clean/restore blindly. Check process names/listeners, not credential-bearing argument lists. If any stage IN_PROGRESS or transcript pending_tool/unansweredtoolcalls, audit actual filesystem/results before resuming; never replay writes blindly. No intended handoff-proof transcript/artifact existed at this checkpoint.

Last verified completed stage: github02:55:16Z. Fresh local_agent acceptance and resume_engine also passed. Bionic native historical acceptance remainsPASS, current usabilityBLOCKED; next unfinished commissioning stage bionic_usability. First small pending verification: source-edited startup-helper/handoff proof. Current host: regular LM Studio with Q4_K_M12544/one slot/Q8KV; previous113152/four-slot native failures are dated. No Codexreload performed; actor of modelchangeunknown. Capture actual load/VRAM before action.

Do not rerun historical native fixture or completed commissioning packages/benchmarks. The Notion payload diagnosis is in reports/BIONIC_CONTEXT_POST_REBOOT.md/json; corrected live verifier is scripts/inspect-bionic-context.py (exit2 until native success). Full native assembly and same-model GUI comparison remain unverified. No native GUI controls were exposed. Finish a supported scoped optional-schema experiment without weakening controls, then native retest, integration and report refresh. Current generator edits were NOT fully rerun; older executive/matrix/machine reports may be stale.

Before any new local acceptance, choose a NEW evidence filename; the revised test refuses overwrite. Before report regeneration, preserve old reports/evidence. Commit only sanitized code/state/handoffs/reports, secret-scan stagedchanges, push only authorized PRIVATE commissioning/main-work, verify local/remote/API SHA. No force-push/merge/deploy. Raw logs/catalogs/config backups/model data remain local and excluded. Exact local evidence paths/hashes are in handoff/progress.json; mark missing on a freshclone. Never printcredentials or monitorclipboard. Security output incidents are documented without values in MASTER_HANDOFF.md and FAILURES.md.
