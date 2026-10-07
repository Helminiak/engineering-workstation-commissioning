# Status at urgent checkpoint

Captured 2026-10-07T03:02:12.743797+00:00. No commissioning tasks IN_PROGRESS. Overall BLOCKED. PASS below includes limited scopes from the source ledger; limitations remain explicit.

| Task | Status | Evidence / limits |
|---|---|---|
| execution | PASS | evidence/execution-20261006T195919664576.json |
| local_agent | PASS | evidence/local_agent-20261007T025321846839.json; limited scope: Fresh API/MCP core engineering tools and optional-failure isolation verified on operator-loaded model. Native Bionic current usability remains a separate blocked stage. Joe-account tools are not an OS sandbox. |
| resume_engine | PASS | evidence/resume_engine-20261007T025235722389.json |
| development | PASS | evidence/development-20261007T005625124624.json |
| github | PASS | evidence/github-20261007T025516478022.json; limited scope: Existing authentication, private repository, authorized task branch and matching commit verified. PR creation/merge/deploy are outside authorization. |
| gpu_llm | PASS | evidence/gpu_llm-20261006T200720454223.json; limited scope: Historical Q6 16K/32K benchmark evidence retained. Current operator-loaded Q4/four-slot config is sampled in BIONIC_CONTEXT_DIAGNOSIS.json; no reload or blind context increase performed. Optional 48K/64K Q6 benchmarks not required for current native overhead diagnosis. |
| scientific | PASS | evidence/scientific-20261006T200743799069.json |
| forensics | PASS | evidence/forensics-20261007T010029000684.json; limited scope: 200K synthetic streaming record verification. Descriptive statistics only. One unexplained Python 3.14 failure retained; controls pass and commissioned forensic interpreter is isolated Python 3.12. |
| mbo | PASS | evidence/mbo-20261007T005718584140.json; limited scope: Synthetic Java/Python foundation, not a CME decoder. Queue/persistence are reference rules; regimes describe volume imbalance, not trading strategies. Measured 200-order depth, not exchange-scale load. |
| security | PASS | evidence/security-20261007T010718024753.json; limited scope: Heuristic secret scan and scoped type checks; GPU wheel advisory coverage incomplete. No private code uploaded. |
| rag | PASS | evidence/rag-20261007T010444028156.json; limited scope: Local synthetic authorized directories; PDF text supported/tested, OCR not included. No personal or external data indexed. |
| end_to_end | BLOCKED | evidence/end_to_end-20261007T012934165343.json |
| bionic_native | PASS | evidence/bionic_native-20261007T020611547142.json |
| bionic_usability | BLOCKED | evidence/bionic_usability-20261007T025603155903.json |
| startup_helper_model_preservation | NOT_TESTED | Source edited to avoid model reload; ShellCheck passed before interruption; end-to-end helper/model proof never ran. |
| local_agent_handoff_proof | NOT_TESTED | Task file exists; intended transcript and proof artifact are absent. No running process. |
| integration_report_refresh | NOT_TESTED | tests/end_to_end.py and scripts/build_reports.py modified but full integration/report generation not run. Older completion reports may be stale; this handoff is authoritative. |

Last verified completed stage: github at 2026-10-07T02:55:16.480484+00:00. Latest attempted stage: bionic_usability, BLOCKED/exit2. Next unfinished: bionic_usability.

## Bionic context overflow diagnosis (2026-10-07, COMPLETE)

| Item | Result |
|---|---|
| Failed request | task 22929 @ 00:10:15Z, 38,297 tokens > 33,280 cap (server log `2026-10-07.1.log:15`) |
| Root cause | Accumulated unbounded tool-result text in one long resumed-session turn: 62 results / 139,372 chars; largest single = unbounded full-file read of `handoff/progress.json` (25,721 chars). NOT the MCP catalog, NOT the Local Workbench call. |
| Duplicate MCP registrations | None active in Bionic; only built-in vs Local Workbench overlap (by design). `context7` + `context7-public` both defined in main-app `~/.lmstudio/mcp.json` (inactive for Bionic; optional cleanup). |
| Fresh-session baseline | 15,447–31,748 tokens, all accepted (truncated=0); peaks ~95% of cap, compaction resets to ~15.4K. Healthy but tight. |
| Token record | Before: 38,297 (rejected). After (min tools, bounded reads): 15,447–31,748 (accepted). |
| MCP sufficiency | Local Workbench alone is sufficient; other MCPs correctly disabled. |
| Context length | NOT increased (operator directive). |
| Evidence | `evidence/bionic-failed-request-22929.json` |
