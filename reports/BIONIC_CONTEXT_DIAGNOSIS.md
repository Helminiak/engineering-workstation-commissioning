# Bionic current context usability — BLOCKED

Historical native engineering acceptance remains PASS. The persisted native trace, report and artifacts were independently reviewed; no native commands were rerun as Codex. Current usability is a separate state.

Actual loaded model: Qwen3.8-27B Q4_K_M, context105472, four parallel slots, full GPU offload. These differ from the historical Q6_K32K benchmark configuration. Baseline GPU memory: total32607MiB, used28688MiB, free3421MiB; later snapshots vary. No context increase was attempted.

| Path | Result | Prompt/request tokens | Evidence |
|---|---|---:|---|
| Bionic native hello at21:59:15 local | Context rejection | 122973 | Persisted native error and matching server log |
| Fresh regular LM Studio CLI hello | PASS, exit0 | 36 | evidence/lmstudio-cli-hello-control.json |
| Fresh plain no-tool API hello, Codex control | PASS | 13 | evidence/bionic-context-api-control.json |
| Pristine Bionic vs regular GUI comparison | NOT_TESTED | Unknown | Operator comparison requested; no desktop controls |

The failing native request exceeds105472 by17501 tokens. Separate tokenizer measurements of the persisted base system text (474tokens) and stored message text (167tokens) are small compared with the backend request. Counts of text fragments are not additive complete chat counts. Dynamic tool schemas/instructions, project context and formatting have not been reconstructed, so no individual connector is proven responsible. Stored hello turns contain earlier entries and do not prove a pristine GUI comparison.

Configuration preservation: 12 files copied to owner-only backups; state/bionic-context-backup.json points to the manifest. Raw backups, app databases and transcripts are excluded from Git. No model/context/plugin/security settings were changed in this diagnosis.

Next: compare pristine GUI chats on the same loaded model and record times; then measure enabled tool payload per project/provider. Prefer diagnosing oversized dynamic content before increasing context with limited VRAM headroom. Preserve native coding execution and the historical acceptance evidence.

Machine-readable details: BIONIC_CONTEXT_DIAGNOSIS.json. Historical native proof: BIONIC_NATIVE_ACCEPTANCE.json. Reproduce with python3 scripts/inspect-bionic-context.py (exit2 while blocked) and python3 scripts/verify-bionic-history.py (historical verification exit0).
