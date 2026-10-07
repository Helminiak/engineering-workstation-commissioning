#!/usr/bin/env python3
"""Read-only context telemetry; never raise context or alter app configuration."""

import datetime
import json
import re
import sqlite3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    loaded = json.loads(
        (ROOT / "evidence/bionic-context-loaded-model.json").read_text()
    )
    gpu = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=memory.total,memory.used,memory.free",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    total, used, free = [int(x.strip()) for x in gpu.split(",")]
    errors = []
    logfile = Path(
        "/home/joe/.lmstudio/apps/bionic/server-logs/2026-10/2026-10-06.1.log"
    )
    for line_no, line in enumerate(logfile.read_text(errors="replace").splitlines(), 1):
        match = re.search(
            r"request \((\d+) tokens\) exceeds the available context size \((\d+) tokens\)",
            line,
        )
        if match:
            requested, context = map(int, match.groups())
            errors.append(
                {
                    "line": line_no,
                    "log_timestamp": line.split("]")[0].lstrip("["),
                    "request_tokens": requested,
                    "available_context": context,
                    "excess_tokens": requested - context,
                }
            )
    sessions = []
    for database in Path("/home/joe/.lmstudio/apps/bionic/projects").glob(
        "*/.internal/ng-sessions.sqlite"
    ):
        with sqlite3.connect(f"file:{database}?mode=ro", uri=True) as conn:
            for sid, stamp, blob in conn.execute(
                "SELECT session_id,updated_timestamp,session_json FROM sessions ORDER BY updated_timestamp DESC LIMIT 2"
            ):
                if stamp < 1791336000000:
                    continue
                config = json.loads(blob)
                sessions.append(
                    {
                        "session_id": sid,
                        "updated_timestamp": stamp,
                        "base_system_prompt_characters": len(
                            config.get("baseSystemPrompt", "")
                        ),
                        "module_count": len(config.get("ngModuleSpecifiers", [])),
                        "user_tool_specifier_count": len(
                            config.get("ngUserToolSpecifiers", [])
                        ),
                        "ui_context_estimate": config.get("contextEstimation", {}).get(
                            "total"
                        ),
                    }
                )
    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "current_usability": "BLOCKED",
        "historical_native_acceptance": "PASS; separately verified from persisted Bionic tool trace",
        "loaded_model": loaded,
        "vram_mib": {"total": total, "used": used, "free": free},
        "backup": json.loads((ROOT / "state/bionic-context-backup.json").read_text()),
        "bionic_server_errors": errors[-12:],
        "bionic_hello_entries": json.loads(
            (ROOT / "evidence/bionic-hello-entries.json").read_text()
        ),
        "session_overhead_metadata": sessions,
        "tokenized_text_components": json.loads(
            (ROOT / "evidence/bionic-context-component-tokens.json").read_text()
        ),
        "plain_api_control": json.loads(
            (ROOT / "evidence/bionic-context-api-control.json").read_text()
        ),
        "regular_lmstudio_cli_control": json.loads(
            (ROOT / "evidence/lmstudio-cli-hello-control.json").read_text()
        ),
        "regular_lmstudio_fresh_gui_comparison": "NOT_TESTED: no desktop controls; operator comparison requested",
        "analysis": {
            "confirmed": "Bionic assembled requests around123K tokens exceed loaded105472-token context; generation is rejected. Same model answers a no-tool API hello with13 prompt tokens and regular CLI hello with36.",
            "component_attribution": "System/tool/history contributions cannot be split exactly from redacted server request logs. Native base prompts are2238 characters and24 module specifiers were persisted. These are metadata, not complete assembled requests.",
            "inference": "Large Bionic-specific request overhead dominates the small input. Optional MCP schemas/instructions and project/session context are candidates; no particular connector is proven responsible.",
            "freshness_limit": "Stored hello entries include earlier entries. API/CLI controls are fresh. Pristine Bionic-versus-LM-Studio GUI comparison is still required.",
            "memory_decision": "No context increase attempted: only about3.3GiB VRAM free under current large-context/four-slot Q4 configuration. Do not reuse earlier Q6/32K memory estimates for this different configuration.",
        },
        "changes": "Workspace evidence/checkpoint writes only. No model, context, plugin, security or app configuration changes.",
        "next_action": "Compare pristine Bionic and regular LM Studio GUI hello requests on the same loaded model. Then measure enabled tool payload per project/provider and test a minimal core-only project without changing global security controls.",
    }
    (ROOT / "reports/BIONIC_CONTEXT_DIAGNOSIS.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    (ROOT / "evidence/bionic-context-diagnosis.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(
        f"BLOCKED: {len(errors)} logged context rejections; loaded context{loaded['models'][0]['contextLength']}; VRAM free{free}MiB. Historical native acceptance retained."
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
