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

- Native Bionic acceptance BLOCKED at submission, not shell execution: normal launch of installed Bionic1.1.7+7 succeeded, but cua.getState still returned apps=[], browsers=[]. No native commands submitted; outputs/exit codes absent. Codex protocol probes of native-config core/Context7-public/Cloudflare pass. Actual launch reports Atlassian MCP authentication required and duplicate GitHub tool names ignored; impact on native core execution unverified. Legacy Context7 OAuth unauthenticated probe fails independently. Fresh existing-repo fixture and exact prompt saved. No security bypass or connector/config change attempted.

- Normal Bionic launch coincided with unloaded commissioned Qwen model: lms ps reported no loaded models, SDK list returned[], GPU memory fell to1833MiB, and CLI commit changed from69d945a to1b7181b. Root mechanism unverified. Restoring existing commissioned Qwen Q6_K32K configuration with scripts/load-commissioning-model.cjs, then checking inference/health. Do not repeat app launches blindly; first inspect current process/model state.

- Post-launch Qwen repair PASS: existing loader exit0 restored Q6_K32768; authenticated API returned expected42 in0.210s. Codex health check exit0. This does not change native Bionic acceptance BLOCKED. Evidence: bionic-launch-inference-repair.json and health-after-bionic-launch.json.

- Current Bionic usability failure after historical acceptance: operator-loaded Q4_K_M105472/four slots uses28688MiB of32607MiB VRAM at baseline. Server rejects hello-related122973-token request (17501 over context); other native requests~123K. Native error persisted in session DB. Base system text tokenizes474, stored message text167; dynamic payload attribution unresolved. Regular CLI hello36tokens and API13tokens pass. No configuration/context increase attempted; 12 files backed up privately. Historical native PASS verified from real tool trace and kept separate. GUI comparison remains pending.

Full integration exits 2 for current Bionic context usability failure. Historical native acceptance, CLI authentication and authorized private remote push verification pass. These are not PASS.
