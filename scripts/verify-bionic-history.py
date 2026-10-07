#!/usr/bin/env python3
"""Verify persisted Bionic-native acceptance evidence; never execute its commands."""

import datetime
import hashlib
import json
import os
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASE = ROOT / "scratch/local-agent-acceptance/bionic-native-20261007T013341"


def main():
    calls = {}
    results = {}
    source = None
    for database in Path("/home/joe/.lmstudio/apps/bionic/projects").glob(
        "*/.internal/ng-sessions.sqlite"
    ):
        with sqlite3.connect(f"file:{database}?mode=ro", uri=True) as conn:
            row = conn.execute(
                "SELECT id FROM chat_entries WHERE entry_json LIKE '%Bionic Native Tool Acceptance Report%' LIMIT 1"
            ).fetchone()
            if not row:
                continue
            source = str(database)
            cursor = row[0]
            seen = set()
            while cursor and cursor not in seen:
                seen.add(cursor)
                row = conn.execute(
                    "SELECT previous_id,entry_json FROM chat_entries WHERE id=?",
                    (cursor,),
                ).fetchone()
                if not row:
                    break
                entry = json.loads(row[1])
                message = entry.get("message", {})
                for part in (
                    message.get("parts", []) if isinstance(message, dict) else []
                ):
                    uid = part.get("uniqueToolCallId")
                    if part.get("type") == "toolCallRequest":
                        calls[uid] = part
                    elif part.get("type") == "toolCallResult":
                        results[uid] = part
                cursor = row[0]
            break
    assert source and calls and results, "Persisted native trace not found"
    trace = []
    for uid, call in calls.items():
        result = results.get(uid)
        text = (
            "\n".join(
                p.get("text", "")
                for p in result.get("result", [])
                if isinstance(p, dict)
            )
            if result
            else None
        )
        match = re.search(r"Exit code:\s*(-?\d+)", text or "")
        trace.append(
            {
                "native_tool": call["name"],
                "parameters": call["parameters"],
                "output": text,
                "exit_code": int(match.group(1)) if match else None,
                "native_error": result.get("details", {}).get("isError", False)
                if result
                else None,
            }
        )
    trace.reverse()

    def shell(fragment, output):
        return any(
            t["native_tool"] == "shell_command"
            and fragment in t["parameters"].get("command", "")
            and t["exit_code"] == 0
            and output in (t["output"] or "")
            for t in trace
        )

    assert shell("whoami", "joe")
    assert shell("pwd", str(CASE))
    assert shell("nvidia-smi", "RTX 5090")
    assert shell("bash check.sh", "bash-ok")
    assert shell("python3 calculation.py", "385")
    assert shell("pytest", "2 passed")
    assert shell("git status", "master")
    assert shell("git diff", "+commissioned-by-bionic")
    assert any(
        t["native_tool"] == "read_file_lines"
        and "native-bionic-verified" in (t["output"] or "")
        for t in trace
    )
    assert (CASE / "tracked.txt").read_text() == "baseline\ncommissioned-by-bionic\n"
    assert (CASE / "probe.txt").read_text().strip() == "native-bionic-verified"
    hashes = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in CASE.iterdir()
        if p.is_file()
    }
    evidence = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "executor": "Bionic native agent (historical)",
        "reviewer": "Codex read-only trace/artifact verification; no acceptance commands rerun",
        "status": "PASS",
        "fixture": str(CASE),
        "source_database": source,
        "native_trace": trace,
        "artifact_sha256": hashes,
        "current_usability": "BLOCKED separately; historical pass is not a current usability guarantee",
    }
    target = ROOT / "evidence/bionic-native-historical-trace.json"
    target.write_text(json.dumps(evidence, indent=2) + "\n")
    os.chmod(target, 0o600)
    # Sanitized records retain native command output and exits, without prompt/history dumps.
    summary = {k: v for k, v in evidence.items() if k != "native_trace"}
    summary["native_commands"] = [
        {
            "command": t["parameters"].get("command"),
            "exit_code": t["exit_code"],
            "native_error": t["native_error"],
            "output_sha256": hashlib.sha256((t["output"] or "").encode()).hexdigest(),
        }
        for t in trace
        if t["native_tool"] == "shell_command"
    ]
    summary["raw_outputs"] = (
        "Local owner-only evidence/bionic-native-historical-trace.json; excluded from Git"
    )
    (ROOT / "reports/BIONIC_NATIVE_ACCEPTANCE.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(
        f"PASS: persisted native tool trace and artifacts verified; {len(summary['native_commands'])} historical shell commands. Current usability remains separately blocked."
    )


if __name__ == "__main__":
    main()
