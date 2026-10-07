import json
import os
import subprocess
import tempfile
from pathlib import Path

script = Path("scripts/commission.py").resolve()
with tempfile.TemporaryDirectory() as d:
    r = Path(d)
    for name in ["commissioning", "evidence", "handoff", "reports"]:
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
    (r / 'reports/BIONIC_CONTEXT_POST_REBOOT.json').write_text(json.dumps({
        'host_status': {'model': {'context_length': 113152}}}))
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
    handoff = (r / 'handoff/CODEX_RESUME.md').read_text()
    assert 'measured context 113152' in handoff
    assert 'operator resumed autonomous commissioning' in handoff
    p['stages']['end_to_end'] = {'status': 'BLOCKED'}
    p['stages']['bionic_usability'] = {'status': 'BLOCKED'}
    (r / 'commissioning/progress.json').write_text(json.dumps(p))
    status = subprocess.check_output(['python3', str(script), 'status'], env=env, text=True)
    assert 'Next unfinished stage: bionic_usability' in status
print("PASS: runner failure, timeout, rerun success, evidence and handoff generation")
