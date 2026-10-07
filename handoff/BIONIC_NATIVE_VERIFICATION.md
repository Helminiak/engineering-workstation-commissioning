# Bionic native acceptance and current usability

Historical native engineering acceptance PASS is preserved. Codex independently reviewed the persisted native tool-call/result trace and fixture artifacts without rerunning native commands. The trace contains 11 shell command results, plus native file reads/writes and one repaired edit-schema error. Bash, Python calculation385, pytest2tests, whoami/pwd/GPU and scoped Git status/diff passed. See reports/BIONIC_NATIVE_ACCEPTANCE.json and private evidence/bionic-native-historical-trace.json. Do not repeat or overwrite that fixture.

Current usability is separately BLOCKED. Read reports/BIONIC_CONTEXT_DIAGNOSIS.json. Current model is operator-loaded Qwen Q4_K_M, context105472, four parallel slots. Bionic requests around123K tokens exceed this context. The hello at21:59:15 produced122973 tokens. Persisted base system prompt tokenizes to474 tokens and stored text through this hello to167; dynamic request components have not been reconstructed. Regular LM Studio CLI hello succeeds with36prompt tokens; plain no-tool API hello succeeds with13. These controls are Codex-run and are not native Bionic commands or GUI comparisons.

Configuration preserved under the directory recorded by state/bionic-context-backup.json (owner-only, excluded from Git). Baseline VRAM total32607MiB/used28688MiB/free3421MiB. No context, model, plugin or security configuration changed during this diagnosis. Do not infer current memory feasibility from the earlier Q6_K32K benchmark.

Next operator action: compare exactly hello in pristine Bionic and regular LM Studio GUI chats on the same loaded local model, without attachments or changed settings. Record timestamps, result and error; correlate with server token counts. Codex has no desktop controls and cannot independently submit those GUI turns. Then inspect per-project enabled tools and quantify assembled schemas/instructions; a minimal core-only test should preserve native coding tools and avoid changing global security controls. No connector has yet been proven responsible for the large request.

Reproduction commands:
```bash
cd /home/joe/LLM-Workspace
lms ps
nvidia-smi --query-gpu=memory.total,memory.used,memory.free --format=csv,noheader
lms chat qwen/qwen3.8-27b --prompt hello --stats --reasoning off --dont-fetch-catalog
python3 scripts/verify-bionic-history.py
python3 scripts/inspect-bionic-context.py
```
The last command exits2 for current blocked usability. Historical acceptance verifier exits0. A health check may pass while Bionic request assembly fails. Never combine these into a current native PASS.

Official coding-project instructions: https://lmstudio.ai/docs/bionic/agent/code-project
