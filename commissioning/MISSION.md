# Operator mission and remaining scope

This is an execution task: inspect, execute, capture exit codes, diagnose, repair (at most three distinct attempts before reassessing), retest and save evidence. Do not infer success from installed files or prior prose. Preserve all existing workspace content. Codex commissions; local Qwen performs routine engineering; ChatGPT reviews architecture. Every agent must resume from disk without conversation history.

## Priority and approval rules

P0: real shell, workspace read/write, Python, Node/npm/npx, local Git/GitHub workflow, optional MCP failure isolation, persistent evidence, independent local engineering acceptance, measured model context. No broad package expansion before this foundation.

Read-only diagnostics and workspace writes are authorized. Obtain operator approval for sudo, drivers, kernel, firmware/BIOS, partitioning, network exposure, security-control changes, destructive system changes, force push, merge and deployment. Creating a new GitHub repository requires authorization and PRIVATE visibility. Existing credentials/integrations must be preserved. Never expose or commit secrets, browser cookies, private datasets or proprietary market data. No trading strategy or proprietary CME data download is authorized.

## Full phase requirements

0. Run whoami, pwd, id, uname, lsb_release, nvidia-smi, free, df and workspace listing; write/read CODEX_EXECUTION_TEST.txt, record separate exit codes. Block normal commissioning if real execution fails.
1. Inspect LM Studio/Bionic versions, native project/shell/filesystem/Git/Python behavior, MCP/Context7 and tool approvals. Prefer native coding mode if actually functional; otherwise use smallest normal-user, audited, loopback execution bridge. Independently test whoami/pwd/nvidia-smi, file write/read, Bash/Python creation/execution, Git status/tracked modification/diff, tests and report. A broken optional tool must not block core execution.
2. State-machine runner: NOT_STARTED, IN_PROGRESS, PASS, PASS_WITH_LIMITATIONS, FAIL, BLOCKED, MANUAL_REQUIRED. Every stage records start/end, commands, exit codes, evidence, verification, repair attempts and remaining issues. Rerunnable verification, no implicit PASS. Resume and status scripts identify next unfinished stage.
3. Inventory then install only missing/broken development utilities and build tools; C/C++/LLVM, Python venv/pipx/uv, supported Node LTS, Java LTS/Maven (Gradle where useful), Rust/Cargo/rustfmt/clippy. Compile/run C++ and Java, pytest, Node, ShellCheck and Rust tests. Avoid conflicting managers; no unnecessary replacements.
4. Separate local Git, authentication, repository read, branch, commit, authorized task-branch push and authorized PR tests. Dedicated private remote only; sanitized scripts/state/manifests/reports. Tests, diff review and secret scan before push. Never force push or merge automatically.
5. Preserve working driver. Inventory toolkit/nvcc, PyTorch, GPU processes and power/temperature. Actual CUDA kernels, allocation, transfers and numerically correct results. LM Studio CLI/model/API/loopback/inference/structured output/tools. Measure 16K/32K, optionally 48K/64K, maintain headroom. Repeated benchmarks with median TTFT, prompt throughput, generation speed, peak VRAM and utilization; identify cache effects.
6. Isolated quantitative environments: NumPy, SciPy, pandas, Polars, Arrow, DuckDB, statsmodels, sklearn, SymPy, numba, plotting/Jupyter, pytest/coverage/Hypothesis, ruff/mypy and justified Optuna. Deterministic linear algebra, seeds, bootstrap CI, Monte Carlo, time series, DataFrames, Parquet, SQL, training and GPU inference. Record actual/expected/tolerance/runtime/memory.
7. Large-log analysis, timestamps/event ordering, anomalies, duplicates/gaps, clock drift/change points, regression/correlation, provenance/hashes and reproducible reports. Synthetic planted anomalies; preserve originals; SHA-256.
8. Synthetic MBO foundation in Java and Python: deterministic event ingestion/replay, sequence checking, add/modify/cancel/partial/full fill/trade, book/price levels, queue, persistence, volumes/delta/regimes. Test missing/out-of-order messages and invalid/crossed books, deletion and determinism. Throughput/memory. No exchange compliance claim from a synthetic reference model.
9. Use useful complementary local quality/security tools, avoid scanner duplication. Evaluate ruff/mypy/ShellCheck, language analysis, dependency audits, secret scanning and SBOM. Software manifest, locks, hashes, versions and reproducibility report. Never upload private code to scanners without approval.
10. Minimum local RAG: authorized directories only, local embeddings, provenance, incremental exact/semantic retrieval, citations and stale detection; text/Markdown/code/JSON/CSV/PDF text as appropriate. Synthetic known answers and measured retrieval quality. No unrelated personal indexing or automatic external uploads.
11. Synthetic integration project: generate/process data, Java compile, Git, tests/statistics/report/evidence hashes/GPU/local LLM/code validation/benchmarks/artifacts. Known answers. Explicit Linux/CPU/RAM/filesystem/GPU/CUDA/LM Studio/Bionic/Bash/Python/Java/Node/Git/GitHub/statistics/forensics/security/RAG/reproducibility/handoff statuses. Keep blocked/untested categories unfinished.

## Continuous checkpoints

After major tasks, before substantial installs, after privileged changes/failures/subsystem verification, roughly every30–45minutes, before large-context work and before stopping. Update STATUS.md, TASKS.md, CHANGELOG.md, NEXT_AGENT.md and progress.json. NEXT_AGENT answers completed/verified/failed/running work, first action, reproduction commands, what not to repeat, approvals, Git commit and log locations. Short local/Codex prompts; persistent files carry instructions.

## Completion artifacts

reports/EXECUTIVE_REPORT.md, VERIFICATION_MATRIX.md, PERFORMANCE_BASELINE.json, FAILURE_REPORT.md, SECURITY_REPORT.md, SYSTEM_ARCHITECTURE.md, INSTALL_MANIFEST.json, MACHINE_READABLE_SUMMARY.json and FINAL_COMMANDS.md; local and Codex handoffs/prompts. Current versions are checkpoint reports, not a declaration of full commissioning.

Health checker must be non-destructive and never repair automatically:0 mandatory pass,1 mandatory failure,2 incomplete/blocked,3 checker failure. Check GPU/CUDA/disk/memory/runtimes/Git/GitHub/LM Studio/workspace/API/critical packages/MCP/dependencies.
