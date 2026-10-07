#!/usr/bin/env python3
"""Evidence-driven stage runner. Explicit verification commands; no implicit PASS."""

import argparse
import datetime
import fcntl
import json
import os
import signal
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(os.environ.get("COMMISSION_ROOT", Path(__file__).resolve().parent.parent))
C = ROOT / "commissioning"
STATES = [
    "NOT_STARTED",
    "IN_PROGRESS",
    "PASS",
    "PASS_WITH_LIMITATIONS",
    "FAIL",
    "BLOCKED",
    "MANUAL_REQUIRED",
]


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def unfinished(p):
    pending = [k for k, v in p['stages'].items()
               if v['status'] not in ('PASS', 'PASS_WITH_LIMITATIONS')]
    for priority in ['bionic_native', 'bionic_usability']:
        if priority in pending:
            pending.remove(priority)
            pending.insert(0, priority)
    return pending


def atomic(path, obj):
    fd, name = tempfile.mkstemp(dir=path.parent)
    with os.fdopen(fd, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(name, path)


def checkpoint(p, note):
    p["updated_at"] = now()
    atomic(C / "progress.json", p)
    done = [
        k
        for k, v in p["stages"].items()
        if v["status"] in ("PASS", "PASS_WITH_LIMITATIONS")
    ]
    pending = unfinished(p)
    diagnosis_path = ROOT / 'reports/BIONIC_CONTEXT_DIAGNOSIS.json'
    if not diagnosis_path.exists():
        diagnosis_path = ROOT / 'reports/BIONIC_CONTEXT_POST_REBOOT.json'
    diagnosis = json.loads(diagnosis_path.read_text()) if diagnosis_path.exists() else {}
    model = (diagnosis.get('actual_loaded_models') or
             [diagnosis.get('host_status', {}).get('model', {})])[0]
    diagnostic_summary = (
        f"Current diagnostic report: reports/BIONIC_CONTEXT_DIAGNOSIS.md/json; "
        f"measured context {model.get('context_length', 'unavailable')}. "
        "Dated schema attribution: reports/BIONIC_CONTEXT_POST_REBOOT.md/json. "
        "Notion is the largest measured MCP schema contributor. Full native request assembly "
        "and regular GUI comparison remain unverified. Saved measurements have their own timestamps; "
        "capture actual load config and VRAM before any model experiment."
        if diagnosis else "Current Bionic diagnosis: reports/BIONIC_CONTEXT_DIAGNOSIS.json."
    )
    next_action = (
        "Read reports/BIONIC_CONTEXT_POST_REBOOT.md/json and preserved configurations. Native UI control is unavailable: record this blocker, continue independent authorized foundation work, and never substitute API/MCP controls for a native GUI result. Do not raise context blindly or disable integrations/security controls."
        if pending and pending[0] == "bionic_usability"
        else (
            "Operator: submit handoff/BIONIC_NATIVE_TASK.txt in native Bionic Allow coding project for the existing fixture repository; preserve native tool transcript and actual exits. Codex: independently review evidence afterward. Do not substitute API/MCP probes for native execution."
            if pending and pending[0] == "bionic_native"
            else "Inspect recorded evidence for the next unfinished stage; rerun its verifier before continuing."
        )
    )
    commit = (
        subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        or "not committed"
    )
    rows = "\n".join(f"- {k}: {v['status']}" for k, v in p["stages"].items())
    (C / "STATUS.md").write_text(
        f"# Status\nCheckpoint: {p['updated_at']}\n{note}\n\n{rows}\n"
    )
    (C / "TASKS.md").write_text(
        "# Tasks\n\n"
        + rows
        + "\n\nNext unfinished: "
        + (pending[0] if pending else "none")
        + "\n"
    )
    with (C / "CHANGELOG.md").open("a") as f:
        f.write(f"\n- {now()}: {note}\n")
    issues = json.loads((C / "open_issues.json").read_text()).get("issues", [])
    branch = (
        subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        ).stdout.strip()
        or "not initialized"
    )
    running = {
        k: v.get("active_command")
        for k, v in p["stages"].items()
        if v["status"] == "IN_PROGRESS"
    }
    text = f"""# Resume commissioning
Objective: verified engineering workstation; execution and handoff before package expansion.
Checkpoint: {p["updated_at"]}
Verified phases: {", ".join(done) or "none"}
Unfinished phases: {", ".join(pending)}
Stage status:\n{rows}
Open issues: {json.dumps(issues)}
Current base commit before this checkpoint: {commit}. Run git log -1 for latest committed state.
Working branch: {branch}.
Currently running stages: {json.dumps(running)}. An IN_PROGRESS record may reflect interruption; inspect process list before reverify. LM Studio localhost API and model are persistent services, see machine_state.json.
First command: scripts/show_status.sh
Read commissioning/MISSION.md for the durable operator requirements.
Current scope: operator resumed autonomous commissioning; continue safe authorized stages without waiting between verified tasks. Preserve credentials, controls, audit logs and completed fixtures. Read the latest AUTHORIZATION.json; older reboot-stop instructions are historical.
Reproduce current blocker: native Bionic UI requires operator verification; read handoff/BIONIC_NATIVE_VERIFICATION.md. Verify private GitHub state with python3 scripts/verify-github-remote.py after authorized pushes. Health checks CLI authentication separately from remote writes. Development passes; do not repeat apt installation.
Next: {next_action}
{diagnostic_summary}
Bionic launch state: state/bionic-native-launch.json is historical; inspect actual host processes before another launch. Native fixture: state/bionic-native-case.json; do not recreate it or replace existing data. Historical native acceptance PASS is recorded separately in reports/BIONIC_NATIVE_ACCEPTANCE.json. Preserve raw backups/catalogs outside Git; backup manifests are referenced by state/bionic-context-loaded-backup.json.
Reproduce: python3 scripts/commission.py verify STAGE --command 'VERIFIER' (inspect progress.json commands).
Do not repeat: working NVIDIA driver, working Node, existing model downloads; do not replace existing integrations.
Standing authorization: reviewed development sudo batch already approved and installed; normal workspace builds/tests/checkpoints authorized. Operator approved private Helminiak/engineering-workstation-commissioning creation and sanitized commissioning/main-work push. Read AUTHORIZATION.json.
New approval required: drivers/kernel/firmware, deleting existing data, security controls, network exposure, repository creation/push outside the approved private commissioning repository/branch, merge/deploy.
Raw stdout/stderr/exit codes: evidence/*.json; tests: tests/; logs: logs/. Raw logs excluded from Git.
Local bridge runs with Joe's full account privileges; workspace cwd is not a security sandbox.
No credentials in Git. No production branch changes. No external uploads of private data.
"""
    (C / "NEXT_AGENT.md").write_text(text)
    for name in ["CODEX_RESUME.md", "LOCAL_LLM_START_HERE.md"]:
        (ROOT / "handoff" / name).write_text(text)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="action", required=True)
    sub.add_parser("status")
    cp = sub.add_parser("checkpoint")
    cp.add_argument("note")
    v = sub.add_parser("verify")
    v.add_argument("stage")
    v.add_argument("--command", required=True)
    v.add_argument("--timeout", type=int, default=180)
    v.add_argument("--limitations", default="")
    v.add_argument("--incomplete-exit-code", type=int, default=None)
    s = sub.add_parser("set")
    s.add_argument("stage")
    s.add_argument("status", choices=STATES)
    s.add_argument("reason")
    a = ap.parse_args()
    with (C / ".runner.lock").open("w") as lock:
        if a.action != "status":
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        p = json.loads((C / "progress.json").read_text())
        if a.action == "status":
            for k, v in p["stages"].items():
                print(k, v["status"])
            print("Checkpoint:", p["updated_at"])
            pending = [(k, p['stages'][k]) for k in unfinished(p)]
            print('Next unfinished stage:', pending[0][0] if pending else 'none')
            print(
                "Current phase:", pending[0][1].get("phase") if pending else "complete"
            )
            verified = [
                (v.get("end_time") or "", k)
                for k, v in p["stages"].items()
                if v["status"] in ("PASS", "PASS_WITH_LIMITATIONS")
            ]
            print("Last verified subsystem:", max(verified) if verified else "none")
            print(
                "Open failures:",
                [k for k, v in p["stages"].items() if v["status"] == "FAIL"],
            )
            print(
                "Blocked/manual tasks:",
                [
                    k
                    for k, v in p["stages"].items()
                    if v["status"] in ("BLOCKED", "MANUAL_REQUIRED")
                ],
            )
            print(
                "Next recommended action:",
                "Read AUTHORIZATION.json and existing installation evidence; run verify-development.sh before considering any additional package changes."
                if pending and pending[0][0] == "development"
                else "Read NEXT_AGENT.md and run next stage verifier.",
            )
            print("Issues:", (C / "open_issues.json").read_text())
            return
        if a.action == "checkpoint":
            checkpoint(p, a.note)
            return
        st = p["stages"][a.stage]
        if a.action == "set":
            if a.status in ("PASS", "PASS_WITH_LIMITATIONS"):
                raise ValueError(
                    "PASS requires a successful verify command; manual status promotion prohibited"
                )
            st["status"] = a.status
            st["remaining_issues"] = [a.reason]
            checkpoint(p, f"{a.stage}: {a.status}: {a.reason}")
            return
        st["status"] = "IN_PROGRESS"
        st["start_time"] = now()
        st["active_command"] = a.command
        checkpoint(p, f"{a.stage}: verification started")
        record = {"stage": a.stage, "start_time": now(), "command": a.command}
        q = subprocess.Popen(
            ["/bin/bash", "-c", a.command],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            stdout, stderr = q.communicate(timeout=a.timeout)
            record.update(exit_code=q.returncode, stdout=stdout, stderr=stderr)
        except subprocess.TimeoutExpired:
            os.killpg(q.pid, signal.SIGTERM)
            try:
                stdout, stderr = q.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(q.pid, signal.SIGKILL)
                stdout, stderr = q.communicate()
            record.update(
                exit_code=124,
                stdout=stdout,
                stderr=stderr + "\nVerification timeout; process group terminated",
            )
        record["end_time"] = now()
        ep = (
            ROOT
            / "evidence"
            / f"{a.stage}-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')}.json"
        )
        atomic(ep, record)
        st["commands"].append(
            {k: record[k] for k in ["command", "exit_code", "start_time", "end_time"]}
        )
        st["evidence"].append(str(ep.relative_to(ROOT)))
        st["end_time"] = now()
        st.pop("active_command", None)
        st["verification"] = record["exit_code"] == 0
        st["status"] = (
            ("PASS_WITH_LIMITATIONS" if a.limitations else "PASS")
            if record["exit_code"] == 0
            else (
                "BLOCKED"
                if a.incomplete_exit_code is not None
                and record["exit_code"] == a.incomplete_exit_code
                else "FAIL"
            )
        )
        st["remaining_issues"] = (
            [a.limitations]
            if a.limitations
            else (
                []
                if record["exit_code"] == 0
                else [
                    "Verifier failed; inspect evidence and persist distinct repair attempts."
                ]
            )
        )
        checkpoint(p, f"{a.stage}: {st['status']}")
        print(record["stdout"])
        print(record["stderr"])
        raise SystemExit(0 if record["exit_code"] == 0 else 1)


if __name__ == "__main__":
    main()
