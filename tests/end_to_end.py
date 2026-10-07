"""Synthetic integration evidence. Missing mandatory subsystems remain incomplete."""

import csv
import hashlib
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = []
commands = [
    ("Linux/Bash/Node/Git", "scripts/local-agent-capability-test.sh"),
    ("state/handoff", "python3 tests/test_runner.py"),
    ("statistics/data", "venvs/quant/bin/python tests/validate_scientific.py"),
    (
        "forensics",
        "venvs/quant/bin/python tests/test_forensics.py && venvs/quant/bin/python tests/test_streaming_forensics.py && venvs/quant/bin/python tests/test_forensic_statistics.py",
    ),
    (
        "MBO Java/Python",
        "python3 tests/test_mbo.py && scripts/verify-java-mbo.sh && python3 tests/test_cross_language_replay.py && python3 tests/test_mbo_analysis.py",
    ),
    ("GPU/CUDA", "venvs/gpu/bin/python tests/validate_cuda.py"),
    (
        "RAG",
        ".venv/bin/python tests/test_rag.py && .venv/bin/python tests/test_rag_formats.py",
    ),
    ("local-agent Java evidence", "python3 tests/verify_agent_java_proof.py"),
    ("Java/C++/Rust", "scripts/verify-development.sh && scripts/verify-build-tools.sh"),
    ("CPU/RAM/filesystem", "python3 tests/validate_hardware.py"),
    ("GitHub authentication", "gh api user --jq .login"),
    ("security/code validation", "scripts/verify-security.sh"),
    (
        "property tests",
        "venvs/quant/bin/python -m pytest -q tests/test_orderbook_properties.py",
    ),
    ("health", "scripts/engineering-health-check --json evidence/health-final.json"),
]
for name, cmd in commands:
    start = time.perf_counter()
    p = subprocess.run(
        ["/bin/bash", "-c", cmd],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    status = (
        "PASS"
        if p.returncode == 0
        else (
            "MANUAL_REQUIRED"
            if name == "GitHub authentication"
            else ("BLOCKED" if name == "health" and p.returncode == 2 else "FAIL")
        )
    )
    rows.append(
        {
            "category": name,
            "status": status,
            "command": cmd,
            "exit_code": p.returncode,
            "seconds": time.perf_counter() - start,
            "stdout": p.stdout,
            "stderr": p.stderr,
        }
    )
    print(name, status, flush=True)
for category, reason in [
    (
        "GitHub remote writes",
        "Private commissioning repository creation and push require operator approval; no remote configured.",
    ),
    (
        "Bionic native UI",
        "Native projects and approval behavior unavailable to automation; API/MCP tested separately.",
    ),
]:
    rows.append(
        {
            "category": category,
            "status": "MANUAL_REQUIRED",
            "reason": reason,
            "command": None,
            "exit_code": None,
        }
    )
p = ROOT / "artifacts/synthetic-engineering.csv"
with p.open("w") as f:
    writer = csv.writer(f)
    writer.writerow(["i", "square"])
    writer.writerows((i, i * i) for i in range(1, 1001))
actual = sum(int(row["square"]) for row in csv.DictReader(p.open()))
assert actual == 333833500
report = {
    "status": "FAIL"
    if any(r["status"] == "FAIL" for r in rows)
    else ("BLOCKED" if any(r["status"] != "PASS" for r in rows) else "PASS"),
    "known_answer": {"sum_squares_1000": actual, "expected": 333833500},
    "artifact_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
    "results": rows,
    "local_llm_evidence": "evidence/local-llm-acceptance.json",
    "limitations": "Local LLM evidence is independently checked; Authorized GitHub remote writes and native Bionic verification gate full integration completion. Native Bionic remains separately unverified. No proprietary data or trading strategy.",
}
(ROOT / "evidence/end-to-end.json").write_text(json.dumps(report, indent=2) + "\n")
(ROOT / "artifacts/engineering-report.json").write_text(
    json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2) + "\n"
)
raise SystemExit(
    1 if report["status"] == "FAIL" else 2 if report["status"] == "BLOCKED" else 0
)
