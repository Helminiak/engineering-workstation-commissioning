#!/usr/bin/env python3
"""Refresh sanitized reports from recorded evidence, never infer verification."""

import datetime
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "commissioning"
R = ROOT / "reports"


def read(name):
    p = ROOT / name
    return json.loads(p.read_text()) if p.exists() else {"status": "NOT_TESTED"}


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n")


def command(argv):
    p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        "command": argv,
        "exit_code": p.returncode,
        "stdout": p.stdout.strip(),
        "stderr": p.stderr.strip(),
    }


now = datetime.datetime.now(datetime.timezone.utc).isoformat()
progress = read("commissioning/progress.json")
versions = {}
for name, args in {
    "git": ["git", "--version"],
    "gh": ["gh", "--version"],
    "node": ["node", "--version"],
    "npm": ["npm", "--version"],
    "npx": ["npx", "--version"],
    "python": ["python3", "--version"],
    "uv": ["uv", "--version"],
    "lmstudio_cli": ["lms", "--version"],
    "gcc": ["gcc", "--version"],
    "g++": ["g++", "--version"],
    "clang": ["clang", "--version"],
    "java": ["java", "-version"],
    "javac": ["javac", "-version"],
    "maven": ["mvn", "-version"],
    "rustc": ["rustc", "--version"],
    "cargo": ["cargo", "--version"],
    "rustfmt": ["rustfmt", "--version"],
    "shellcheck": ["shellcheck", "--version"],
    "cmake": ["cmake", "--version"],
    "ninja": ["ninja", "--version"],
    "gdb": ["gdb", "--version"],
    "valgrind": ["valgrind", "--version"],
    "ccache": ["ccache", "--version"],
    "hyperfine": ["hyperfine", "--version"],
}.items():
    versions[name] = command(args)
packages = {}
for name, python in [
    ("local-agent", ".venv/bin/python"),
    ("quant", "venvs/quant/bin/python"),
    ("gpu", "venvs/gpu/bin/python"),
]:
    p = subprocess.run(
        ["uv", "pip", "list", "--python", python, "--format", "json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    packages[name] = json.loads(p.stdout) if p.returncode == 0 else []
manifest = {
    "timestamp": now,
    "tools": versions,
    "python_environments": packages,
    "reviewed_system_packages": read("evidence/development-package-state.json"),
    "changes": "User-local gh installed with official SHA-256; isolated quant and gpu environments installed; reviewed system development batch installed and functionally verified; existing Node, local-agent environment, drivers and integrations preserved.",
}
write(R / "INSTALL_MANIFEST.json", manifest)
write(C / "installed_tools.json", {"tools": versions, "python_environments": packages})
info = subprocess.run(
    ["node", "scripts/model-info.cjs"],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
)
machine = {
    "timestamp": now,
    "username": command(["whoami"])["stdout"],
    "hostname": command(["hostname"])["stdout"],
    "kernel": command(["uname", "-r"])["stdout"],
    "distribution": command(["lsb_release", "-ds"])["stdout"],
    "cpu_model": next(
        (
            line.split(":", 1)[1].strip()
            for line in Path("/proc/cpuinfo").read_text().splitlines()
            if line.startswith("model name")
        ),
        "unknown",
    ),
    "logical_cpus": os.cpu_count(),
    "ram_kib": int(Path("/proc/meminfo").read_text().splitlines()[0].split()[1]),
    "disk_free_bytes": shutil.disk_usage(ROOT).free,
    "gpu": command(
        [
            "nvidia-smi",
            "--query-gpu=name,driver_version,memory.total,memory.used",
            "--format=csv,noheader",
        ]
    )["stdout"],
    "lmstudio_version": json.loads(
        Path("/opt/LM-Studio/resources/app/package.json").read_text()
    )["version"],
    "bionic_version": json.loads(
        Path("/opt/Bionic/resources/app/package.json").read_text()
    )["version"],
    "loaded_llms": json.loads(info.stdout) if info.returncode == 0 else [],
    "model_hashes": read("evidence/model-hashes.json"),
    "cuda_toolkit_nvcc": shutil.which("nvcc")
    or "NOT_INSTALLED; PyTorch wheels provide tested runtime",
}
write(C / "machine_state.json", machine)
verification = {
    "timestamp": now,
    "local_execution": read("evidence/phase0.json").get("timestamp"),
    "local_agent": "Historical API/MCP and native acceptance PASS; current Bionic usability BLOCKED separately",
    "cuda": read("evidence/cuda-validation.json"),
    "scientific": read("evidence/scientific-validation.json"),
    "forensics": read("evidence/forensics-validation.json"),
    "mbo": read("evidence/mbo-validation.json"),
    "streaming_forensics": read("evidence/streaming-forensics.json"),
    "forensic_statistics": read("evidence/forensic-statistics.json"),
    "cross_language_replay": read("evidence/cross-language-replay.json"),
    "local_agent_java": read("evidence/local-agent-java-verification.json"),
    "bionic_native": read("reports/BIONIC_NATIVE_ACCEPTANCE.json"),
    "bionic_current_usability": read("reports/BIONIC_CONTEXT_DIAGNOSIS.json"),
    "github_connector": read("evidence/github-connector.json"),
    "github_cli_read": read("evidence/github-cli-read.json"),
    "github_remote": read("evidence/github-remote-verification.json"),
    "rag_formats": read("evidence/rag-formats.json"),
    "hardware": read("evidence/hardware-validation.json"),
    "rag": {
        k: v for k, v in read("evidence/rag-validation.json").items() if k != "results"
    },
    "end_to_end": {
        k: v for k, v in read("evidence/end-to-end.json").items() if k != "results"
    },
    "health": {
        k: v["status"]
        for k, v in read("evidence/health-final.json").get("checks", {}).items()
    },
}
write(C / "verification.json", verification)
benchmarks = {
    str(n): {
        k: v for k, v in read(f"evidence/llm-benchmark-{n}.json").items() if k != "rows"
    }
    for n in [16384, 32768]
}
benchmarks["recommended_context"] = 32768
benchmarks['recommended_context_scope'] = 'Historical Q6 API/MCP benchmark only; never automatically apply to current operator-loaded Q4/native Bionic.'
benchmarks["mbo_python_mixed"] = read("evidence/mbo-mixed-benchmark.json")
benchmarks["mbo_java_mixed"] = read("evidence/java-mbo-mixed-benchmark.json")
benchmarks["mbo_benchmark_limits"] = (
    "200-order synthetic depth, different Python/Java implementations; not an exchange-scale or apples-to-apples language benchmark. Java trials show JIT/GC variability."
)

benchmarks["long_input_tokens"] = read("evidence/long-context.json").get("input_tokens")
benchmarks["notes"] = (
    "Generation and TTFT include shared-prefix cache effects. Long-input run initially took 10.073s; repeat was cached. No cold prompt-throughput or 48K/64K claim."
)
write(R / "PERFORMANCE_BASELINE.json", benchmarks)
commit = command(["git", "rev-parse", "HEAD"])["stdout"]
summary = {
    "timestamp": now,
    "status": "FAIL"
    if any(v["status"] == "FAIL" for v in progress["stages"].values())
    else (
        "BLOCKED"
        if any(
            v["status"] not in ("PASS", "PASS_WITH_LIMITATIONS")
            for v in progress["stages"].values()
        )
        else "PASS_WITH_LIMITATIONS"
    ),
    "base_commit": commit,
    "branch": command(["git", "branch", "--show-current"])["stdout"],
    "stages": {k: v["status"] for k, v in progress["stages"].items()},
    "open_issues": read("commissioning/open_issues.json")["issues"],
    "verification": verification,
    "performance": benchmarks,
}
write(R / "MACHINE_READABLE_SUMMARY.json", summary)
# Minimal package SBOM: versioned packages, without credentials or raw logs.
components = []
for env, pkgs in packages.items():
    for p in pkgs:
        components.append(
            {
                "type": "library",
                "bom-ref": f"{env}:{p['name']}@{p['version']}",
                "name": p["name"],
                "version": p["version"],
                "properties": [{"name": "commissioning:environment", "value": env}],
            }
        )
write(
    R / "SBOM.cdx.json",
    {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "components": components,
    },
)
hashes = {
    str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
    for folder in ["scripts", "tests", "configs"]
    for p in sorted((ROOT / folder).rglob("*"))
    if p.is_file() and "__pycache__" not in str(p)
}
for p in sorted((ROOT / "tools").glob("commissioning*.py")) + [
    ROOT / "tools/workbench_mcp.py"
]:
    hashes[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
write(R / "CONFIGURATION_HASHES.json", hashes)
rows = "\n".join(
    f"| {k} | {v['status']} | {'; '.join(v['remaining_issues']) or 'Recorded verifier evidence in progress.json'} |"
    for k, v in progress["stages"].items()
)
(R / "VERIFICATION_MATRIX.md").write_text(
    "# Verification matrix\n\n| Phase | Status | Scope / remaining work |\n|---|---|---|\n"
    + rows
    + "\n\nPASS applies only to recorded verifiers. MANUAL_REQUIRED and BLOCKED are unfinished. Raw per-command evidence remains local under evidence/.\n"
)
(R / "EXECUTIVE_REPORT.md").write_text("""# Commissioning checkpoint report
The core local-agent execution and persistent handoff infrastructure is operational and verified. Full workstation commissioning remains incomplete.

Verified: Joe/5090FE/Ubuntu 26.04.1/RTX 5090; real shell and file writes; Node/npm/npx; local Git branching and commits; Qwen independent engineering acceptance via API/MCP; Context7 public initialization and optional-connector failure isolation; rerunnable stage engine with timeout/failure evidence; PyTorch CUDA kernels and transfers; deterministic scientific validation; 200K-record disk-backed forensic analysis and correlation/regression fixtures; Java/Python order-book agreement, Maven/JUnit, CMake/Ninja, clang analysis, Valgrind, GDB, Rust/clippy and ShellCheck; local-agent Java compilation; local embedding retrieval and stale-index detection.

Historical API/MCP Qwen Q6_K recommendation: 32,768, tested with 25,729 input tokens. This is not a fix for current Bionic request overhead. Measured short benchmark peak VRAM 25,725 MiB of 32,607 MiB; median generation about 161 tokens/sec. Cache and short-prompt limits apply.

Private Helminiak/engineering-workstation-commissioning created with operator approval; commissioning/main-work push verified by matching local HEAD, Git remote and GitHub API commits. CLI authentication and private repository permissions pass. Historical native acceptance PASS retained. Fresh post-reboot API/MCP acceptance passed independently with real shell/file/Bash/Python/Git/Node execution and optional-connector failure isolation. Native Bionic remains BLOCKED: fresh hello122973tokens exceeded operator-loaded Q4_K_M113152/four slots by9821. Measured catalogs contain223tools; actual-template synthetic hello114825tokens, without Notion54952. Notion is the largest measured contributor; full native assembly and regular GUI comparison remain unverified. No model/context/plugin/security changes made. Read BIONIC_CONTEXT_DIAGNOSIS.json for latest telemetry and BIONIC_CONTEXT_POST_REBOOT.md for dated payload attribution. Full integration remains incomplete. PR creation, merge/deploy remain outside authorization. One unexplained Python3.14 streaming failure remains recorded; forensic runtime is isolated Python3.12. Missing optional yq/fd/Gradle did not prevent verified workflows.

Read commissioning/NEXT_AGENT.md and run scripts/show_status.sh. Detailed evidence is local in evidence/ and logs/. Sanitized reports, scripts and state are committed locally and pushed to the approved private repository. See git log -1 for the exact latest commit.
""")
(R / "FAILURE_REPORT.md").write_text(
    (C / "FAILURES.md").read_text()
    + "\nFull integration exits 2 for current Bionic context usability failure. Historical native acceptance, CLI authentication and authorized private remote push verification pass. These are not PASS.\n"
)
(R / "SYSTEM_ARCHITECTURE.md").write_text(
    (C / "ARCHITECTURE.md").read_text()
    + """\n## Actual execution paths
scripts/local_agent.py uses the loopback authenticated OpenAI-compatible API and an independent stdio core MCP session. Optional connectors are excluded. Bionic native Connected Apps remains configured but its UI and approval mode are not verified.

scripts/commission.py persists stage start/end, command, exit status, stdout/stderr evidence, outcomes and issues. It updates handoffs and status; interrupted tool actions require reconciliation, not blind replay. transcripts in state/ and command audits in logs/local-agent/ are local and excluded from Git.

Environments: .venv retains original local-agent tools; venvs/quant is Python 3.12 scientific/tooling; venvs/gpu is Python 3.12 with CUDA 13.0 PyTorch. Lock manifests are in configs/. Existing startup helpers can reload old context/quantization settings. Preserve the operator-loaded model; invoke .venv/bin/python scripts/local_agent.py directly for bounded core tasks when the model is already loaded. Do not start both native apps or change context blindly.
"""
)
(R / "SECURITY_REPORT.md").write_text("""# Security checkpoint
Local API is bound to 127.0.0.1:1234 and uses the existing owner-only token. Credential values are excluded from saved reports, source and commits. An early SDK handle dump exposed transient session fields; a later metadata probe accidentally printed a credential-bearing auth field. Both incidents are recorded; corrected probes use whitelisted metadata. No credential values were written into checkpoints/Git and no credential changes made. Original bridge/configurations preserved. Audit logs/transcripts/raw catalogs remain owner-only and excluded from Git. Redaction is heuristic; never upload raw logs blindly.

Core execution is Joe-account shell execution, not an OS sandbox. Cwd and document reads are scoped; arbitrary executable code can reach other user files. Agent prompts prohibit sudo and external actions, but prompts are not a hard security boundary. Privileged changes require operator approval. Historical native tool acceptance passed with recorded outputs/exits. Current Bionic usability is blocked separately; ongoing approval coverage remains limited.

ruff and limited mypy checks are recorded. Quant and local-agent pip-audit scans and npm audit found no known vulnerabilities at scan time. The GPU vendor wheel index is not fully covered by PyPI advisory scanning. The staged secret scan is heuristic and does not replace Gitleaks. ShellCheck, clang analysis, Java lint/JUnit and Rust clippy now pass. No private code was sent to third-party scanners; dependency auditing queried public package names.

Rollback: backups/workbench_mcp.*.py restores the original bridge; stop local agent before restoring. New isolated environments can be retired independently after confirming no tasks use them. The user-local gh binary is independent of system packages. No account integrations were removed, credentials changed, or ports exposed.
""")
(R / "FINAL_COMMANDS.md").write_text("""# Resume and verification commands
```bash
cd /home/joe/LLM-Workspace
scripts/show_status.sh
scripts/engineering-health-check --json evidence/health-current.json
.venv/bin/python scripts/local_agent.py tests/local-agent-task.txt --transcript state/new-agent-task.json
.venv/bin/python tests/local_llm_acceptance.py --evidence evidence/acceptance-NEW-UNUSED-NAME.json
python3 tests/end_to_end.py
scripts/verify-before-commit.sh
git log -1
```
Integration exit 2 means incomplete. Health checks mandatory local subsystems and CLI authentication; health exit 0 does not prove remote write access or native Bionic behavior.

The reviewed apt batch is already approved, installed and verified; do not repeat it. Run scripts/verify-development.sh and scripts/verify-build-tools.sh for verification. CLI authentication as Helminiak is verified. The private commissioning repository and commissioning/main-work pushes are authorized and verified. Run python3 scripts/verify-github-remote.py after pushes. Other repositories/branches and merge/deploy require separate authorization.
""")
(R / "REPRODUCIBILITY_REPORT.md").write_text("""# Reproducibility
Exact currently installed Python versions are frozen in configs/*-requirements.lock. Recreate isolated Python 3.12 environments with uv venv, then install the matching lock; the GPU lock requires the official cu130 PyTorch wheel index. Locks list versions but do not lock every wheel hash; platform-specific reproducibility is limited. CONFIGURATION_HASHES.json records source/config hashes and SBOM.cdx.json records packages per environment. SHA-256 source-evidence hashes and seeded validation are recorded locally. Raw datasets are excluded from Git; tests regenerate synthetic fixtures.

Sanitized state is available in the approved private Helminiak/engineering-workstation-commissioning repository on commissioning/main-work; verify remote commit against local HEAD after pushes. Previous Qwen setup documentation may be stale; commissioned settings/evidence are authoritative. Benchmark medians include prefix caching and do not represent cold long-context prompt throughput.
""")
print("Reports refreshed with actual incomplete statuses")
