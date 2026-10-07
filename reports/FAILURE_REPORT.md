# Failures
- Earlier restricted session could not communicate with NVIDIA driver; unrestricted session retest passes. Do not repair driver based on that obsolete result.
- gh CLI absent; authentication and remote workflow remain unverified.

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

Full integration exits 2 for unfinished system tools and GitHub authentication; these are not PASS.
