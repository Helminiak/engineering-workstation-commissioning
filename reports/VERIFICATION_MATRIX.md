# Verification matrix

| Phase | Status | Scope / remaining work |
|---|---|---|
| execution | PASS | Recorded verifier evidence in progress.json |
| local_agent | PASS_WITH_LIMITATIONS | Native Bionic UI projects, shell and approval behavior require operator verification. API/MCP agent and optional connector failure isolation verified. |
| resume_engine | PASS | Recorded verifier evidence in progress.json |
| development | MANUAL_REQUIRED | Inventory and apt simulation saved. Node/Python/Git functional. Missing C/C++/Java/Rust and utilities require operator-approved sudo apt batch. |
| github | MANUAL_REQUIRED | gh installed and SHA-256 verified. gh auth status exits 1: no logged-in GitHub hosts. Operator sign-in needed; no remote created. |
| gpu_llm | PASS_WITH_LIMITATIONS | 16K/32K measured; 48K/64K not tested. Short inference performance only. CLI/SDK allocation registry differs from native REST. Bionic native UI unverified. |
| scientific | PASS | Recorded verifier evidence in progress.json |
| forensics | PASS_WITH_LIMITATIONS | Synthetic baseline validates known anomalies; current JSONL analyzer loads records in memory and is not yet a large-log streaming implementation. |
| mbo | MANUAL_REQUIRED | Python synthetic reference book unit tests pass; Java implementation and compilation require JDK approval. Full order-book throughput, liquidity/regime analysis not yet commissioned. |
| security | PASS_WITH_LIMITATIONS | Heuristic secret scan, limited domain mypy and package audits only. GPU vendor advisory coverage incomplete; native approval and hard execution sandbox unverified; ShellCheck pending JDK/tool batch. |
| rag | PASS_WITH_LIMITATIONS | Tested synthetic authorized directory; no OCR, long-document retrieval benchmark or personal-data indexing. |
| end_to_end | BLOCKED | Available subsystems verified; Java/C++/Rust and GitHub are mandatory unfinished gates. |

PASS applies only to recorded verifiers. MANUAL_REQUIRED and BLOCKED are unfinished. Raw per-command evidence remains local under evidence/.
