# Bionic context overhead after reboot

Reboot and the authorized private checkpoint verified. Local/remote commit at resume: `3bf90445792ac25bde35d5da6a9bd5d74b9d6c6b`. Boot time: 2026-10-06 22:16:56 local. Historical native acceptance remains PASS; no commissioning stage or historical fixture was rerun.

Bionic is running, its API/SDK listeners are loopback, and **initially no model was loaded**. The initial sample had no loaded context; the operator subsequently loaded Q4_K_M113152/four slots, detailed below. Host RTX 5090 / driver 595.91.07 is healthy. First unloaded sample: 32607 MiB total, 1310 used, 30799 free. Second: 1293 used, 30815 free. Sandboxed NVIDIA/API failures were environment restrictions. Neither sample measures loaded-model feasibility.

Fresh Bionic versus regular LM Studio GUI comparison: **PARTIAL**. Bionic failure is now measured; regular GUI result/time pending. No native GUI control surfaces are exposed, regular LM Studio GUI is absent, and initially no model was loaded. Operator subsequently provided the Bionic failure. Regular GUI time/result requested. The old 122973-token rejection against context105472 and earlier API13/CLI36 controls remain historical; they are not post-reboot tests.

Read-only MCP initialize/list-tools probes measured the following catalogs, without tool calls or credential refresh. Existing cached filesystem/Playwright entry points were used directly; no npx fetch/install occurred. Counts use compact OpenAI-style function JSON including name, description and input schema, before Bionic filtering/name rewriting and the Qwen chat template.

| Provider | Tools | Function JSON characters | Instructions characters |
|---|---:|---:|---:|
| Linear | 68 | 86,528 | 188 |
| Notion | 47 | 226,564 | 2,060 |
| Sentry | 14 | 38,066 | 0 |
| GitHub | 46 | 50,863 | 1,802 |
| Workspace Files | 14 | 8,407 | 0 |
| Playwright Browser | 25 | 18,341 | 0 |
| Local Workbench | 5 | 3,130 | 216 |
| Context7 Docs | 2 | 4,646 | 632 |
| Cloudflare Docs | 2 | 1,063 | 0 |
| Total measured | 223 | 437,608 | 4,898 |

Atlassian was not measured because no existing OAuth token was available; no login was attempted.

**Oversized payload identified:** Notion accounts for approximately 52% of measured function JSON. The `notion-query-data-sources` input schema alone is 78,255 characters; description adds 1,977. The other large input schemas are `notion-query-meeting-notes` (20,421) and `notion-query-sessions` (17,238). The data-source query schema has 537 description instances, 43 unique descriptions, 24,063 characters of repeated descriptions and nesting depth32. Nested filter schemas are a concrete source of large dynamic tool payload.

This identifies the largest measured catalog contributor; **exact native token attribution is pending**. Loaded Qwen tokenizer measurements are now available below. Character counts remain distinct from token counts. Fresh catalogs cannot prove historical content. Saved session module count24, small static base text and session estimates likewise do not reconstruct a complete native request.

Both SHA-256 backup manifests verified. Twelve current configurations saved to `backups/bionic-context-20261007T023211Z/manifest.json`, with directory0700/files0600; only the two model-data files differ from the pre-reboot backup. Raw catalogs are owner-only and Git-ignored. A probe accidentally printed a credential-bearing auth field to tool output; it was corrected, and the value is excluded from reports, checkpoints and Git. No credential changes performed.

Next: obtain regular LM Studio GUI hello result/time on the same operator-loaded model; capture actual context/slots/offload and VRAM for that request. Correlate server counts and tokenize captured provider schemas before a scoped optional-tool experiment. Keep core coding tools and original configuration. No model/context/plugin/security/driver changes made. Do not run automatic commissioning stages or the Q6/32K starter.

## Fresh operator hello and loaded-model token attribution

At 22:38:08 local (2026-10-07T02:38:08Z), the Bionic server rejected **122973 tokens against context113152**, excess **9821**. Operator-reported hello error correlates with log line35773. The current committed session chain has only four entries: a fresh automatic context message, state change, user hello, error; timestamps begin22:38:05.358. This excludes long prior conversation history from the current committed chain; hidden/native dynamic assembly is still not persisted in full. UI context estimate6186 is far below the backend request count.

Actual operator-loaded model: Qwen3.8-27B Q4_K_M, context113152, four parallel slots, full GPU offload, unified KV cache, KV offloaded to GPU, no explicit K/V cache quantization. This context differs from the saved pre-reboot105472; Codex did not change it. Loaded VRAM samples: used28645/free3464, used28720/free3389, then used28888/free3220 MiB (total32607). Samples fluctuate; they do not establish that another context increase fits.

The loaded model tokenizer measures **99706 tokens** for combined compact function JSON. Provider counts: Notion51547, Linear20446, GitHub11214, Sentry8913, Playwright3899, Workspace Files1737, Context71010, Local Workbench686, Cloudflare271. Notion data-source query input schema alone: **16284tokens**. Per-component counts are not exact additive chat counts.

The actual loaded template inlines each tool using `tool | tojson`. Formatter/tokenizer-only measurements, with user hello and no native Bionic base/module context:

| Synthetic input | Tools | Formatted tokens |
|---|---:|---:|
| hello_no_tools | 0 | 53 |
| hello_all_measured_mcp_catalogs | 223 | 114,825 |
| hello_measured_catalogs_without_notion | 176 | 54,952 |
| hello_local_workbench_catalog_only | 5 | 1,067 |

All measured catalogs alone are **1673tokens over current context**; removing Notion from the synthetic formatter input saves **59873tokens**. The oversized dynamic tool schemas are sufficient to exceed the model capacity before native modules. This identifies Notion nested schemas as the largest measured contributor. It does not prove the exact122973-token native assembly: Bionic filtering/name rewriting, built-in modules and instructions remain unmeasured. Synthetic53-token hello is not a regular GUI control. No model inference or tool execution was performed by these measurements.

Current loaded-state settings preserved again in `backups/bionic-context-20261007T024134Z/manifest.json`; directory0700/files0600, SHA-256 manifest. Native regular GUI comparison remains pending. No setting changes or completed commissioning reruns.

Second operator error: newest rejection is in Bionic server log at22:41:18local, line35865:122975tokens against113152context (excess9823). Regular GUI was absent in host process inventory; no fresh regular server rejection found. The operator has not yet confirmed which UI produced the second pasted error, so it is not classified as a regular GUI test. Latest GPU sample:28742used/3367free MiB.
