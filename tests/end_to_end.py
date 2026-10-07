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
    ("forensics", "python3 tests/test_forensics.py"),
    ("MBO Python", "python3 tests/test_mbo.py"),
    ("GPU/CUDA", "venvs/gpu/bin/python tests/validate_cuda.py"),
    ("RAG", ".venv/bin/python tests/test_rag.py"),
    ("Java/C++/Rust", "scripts/verify-development.sh"),
    ("GitHub", "gh auth status"),
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
            if name in ["Java/C++/Rust", "GitHub"]
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
    "limitations": "Local LLM acceptance is separately rerunnable; Java/system tools and GitHub gate completion. No proprietary data or trading strategy.",
}
(ROOT / "evidence/end-to-end.json").write_text(json.dumps(report, indent=2) + "\n")
(ROOT / "artifacts/engineering-report.json").write_text(
    json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2) + "\n"
)
raise SystemExit(
    1 if report["status"] == "FAIL" else 2 if report["status"] == "BLOCKED" else 0
)
