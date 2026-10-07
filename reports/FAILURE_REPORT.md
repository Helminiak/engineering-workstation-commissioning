# Failures
- Earlier restricted session could not communicate with NVIDIA driver; unrestricted session retest passes. Do not repair driver based on that obsolete result.
- Initially gh CLI absent; user-local CLI installed and version verified. CLI authentication and remote write workflow remain unverified; connected GitHub app authentication/read now pass.

- Local acceptance harness first attempt failed: installed MCP SDK exposes input_schema/is_error, not camelCase. Adapted client; no server/config change required.

- 16K benchmark first attempt failed before recording results: overly strict output-content assertion with 300-token cap. Retesting with explicit off reasoning and larger output cap; no performance claimed from failed run.
- Development apt simulation: clippy package name absent; inspect available rust-clippy package before installation. No packages changed.

- Benchmark second repair rejected by API (400): OpenAI-compatible reasoning_effort accepts none, not native off. Reassessed using documented route and direct request; none produces visible text with zero reasoning. Third attempt will retain streamed failure evidence.

- Initial health checker falsely required pip in a uv-managed venv and imported MCP using system Python. Fixed checker to use uv dependency validation and venv MCP client; no environment repair necessary. Native REST loaded_instances is empty for SDK-loaded Q6 variant despite CLI/SDK and inference success; now use explicit SDK metadata, preserve limitation.

- Early SDK diagnostic serialized an SDK handle with transient session credential fields. Switched all diagnostics to whitelisted model metadata; never repeat SDK handle dumps. Persistent API token was not printed. These transient fields were not written into commissioning files.
- Long-input fixture preflight rejected 36159 tokens before API call; reduced to25729 tokens, verified exact answer at32K.
- Scoped mypy initially lacked pypdf in quant environment; installed pypdf, reran successfully.

- Local Qwen scientific task first tool call exited1: scipy.linalg.cond does not exist. Qwen diagnosed it and changed to numpy.linalg.cond; original calculation and regression checks passed. Five tool calls recorded with exit codes[1,0,0,0,0]; independently verified results2,3,385,285.
- Runner handoff enrichment briefly introduced a malformed f-string; syntax and isolated runner tests caught it before any real state update. Simplified precomputed fields, fixed and retested.

- Approved development batch stopped at sudo authentication prompt. No password entered and no apt installation began; interrupted safely. Resolved: operator subsequently ran the approved batch; matching completed apt history and installed package evidence verified. Do not repeat installation.

- Java synthetic book first test exited1: trade events have no order ID, and TreeMap.get(null) throws. Guarded nullable IDs and made side/aggressor validation null-safe. Original test and complete book regression suite rerun. See evidence/mbo-java-attempt1.json.

- Local Java agent compiled/executed successfully but inspected the pre-existing acceptance repo instead of the commissioning repo. Independent review rejected that part; sent exact root-repo commands for correction. Corrected via persistent transcript resume and independently verified root branch/status. No repository created.

- Streaming forensic verifier had one unexpected Python3.14 KeyError (reported key forensic-index- at a sequence lookup) after formatting. Identical3.14 control rerun and isolated3.12 rerun both passed with matching source hashes; JIT was disabled. Root cause is undetermined (runtime/cache or transient input remain alternatives). Pin commissioned forensic workload to isolated3.12 and retain raw failed runner evidence; do not claim the anomaly explained.

- Fresh acceptance retest rejected by independent verifier: model saw an old parent tracked-file diff and claimed it had appended the new case file without doing so. The new file remained baseline. Strengthened exact-case path instructions and scoped independent diff verification. Failed transcript preserved in evidence/local-llm-acceptance-failed-scope.json; model final claims are not proof.

Full integration exits 2 for unfinished native Bionic UI verification. CLI authentication and authorized private remote push verification pass. These are not PASS.
