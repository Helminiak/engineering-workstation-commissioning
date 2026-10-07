import json
import os
import subprocess
import tempfile
from pathlib import Path

script = Path("scripts/commission.py").resolve()
with tempfile.TemporaryDirectory() as d:
    r = Path(d)
    for name in ["commissioning", "evidence", "handoff"]:
        (r / name).mkdir()
    p = {
        "stages": {
            "fixture": {
                "status": "NOT_STARTED",
                "commands": [],
                "evidence": [],
                "remaining_issues": [],
            }
        }
    }
    (r / "commissioning/progress.json").write_text(json.dumps(p))
    (r / "commissioning/open_issues.json").write_text('{"issues":[]}')
    env = dict(os.environ, COMMISSION_ROOT=d)

    def run(cmd, expected):
        q = subprocess.run(
            [
                "python3",
                str(script),
                "verify",
                "fixture",
                "--command",
                cmd,
                "--timeout",
                "1",
            ],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert q.returncode == expected, q

    run("exit 7", 1)
    p = json.loads((r / "commissioning/progress.json").read_text())
    assert p["stages"]["fixture"]["status"] == "FAIL"
    assert p["stages"]["fixture"]["commands"][-1]["exit_code"] == 7
    run("sleep 10", 1)
    p = json.loads((r / "commissioning/progress.json").read_text())
    assert p["stages"]["fixture"]["commands"][-1]["exit_code"] == 124
    run("printf verified", 0)
    p = json.loads((r / "commissioning/progress.json").read_text())
    assert p["stages"]["fixture"]["status"] == "PASS"
    assert len(p["stages"]["fixture"]["evidence"]) == 3
    assert (r / "handoff/CODEX_RESUME.md").exists()
print("PASS: runner failure, timeout, rerun success, evidence and handoff generation")
