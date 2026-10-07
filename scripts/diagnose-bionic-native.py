#!/usr/bin/env python3
"""Codex diagnostics only: never substitute these probes for Bionic-run acceptance."""

import asyncio
import datetime
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

ROOT = Path(__file__).resolve().parent.parent
NATIVE = Path("/home/joe/.lmstudio/apps/bionic/.internal")


def error_types(error):
    result = [type(error).__name__]
    for child in getattr(error, "exceptions", ()):
        result.extend(error_types(child))
    status = getattr(getattr(error, "response", None), "status_code", None)
    if status:
        result.append(f"HTTP_{status}")
    return result


async def probe(name, connection):
    try:
        async with asyncio.timeout(25):
            if connection["type"] == "stdio":
                params = StdioServerParameters(
                    command=connection["command"],
                    args=connection.get("args", []),
                    env=connection.get("env") or None,
                    cwd=connection.get("cwd") or str(ROOT),
                )
                async with (
                    stdio_client(params) as streams,
                    ClientSession(*streams) as client,
                ):
                    await client.initialize()
                    tools = await client.list_tools()
            else:
                # Public availability only; native OAuth credential state is not borrowed or inspected.
                async with (
                    streamable_http_client(connection["url"]) as streams,
                    ClientSession(streams[0], streams[1]) as client,
                ):
                    await client.initialize()
                    tools = await client.list_tools()
        return {
            "name": name,
            "initiator": "Codex",
            "status": "PASS",
            "tools": [t.name for t in tools.tools],
            "scope": "protocol initialization/list only; no Bionic native command execution",
        }
    except Exception as e:  # noqa: BLE001 -- record nested transport failures without credential-bearing tracebacks
        return {
            "name": name,
            "initiator": "Codex",
            "status": "FAIL",
            "error_types": error_types(e),
        }


async def main():
    servers = json.loads((NATIVE / "ng-mcp.json").read_text())["servers"]
    selected = [
        s
        for s in servers
        if s["name"] in ["Local Workbench", "Context7 Docs", "Cloudflare Docs"]
    ]
    results = await asyncio.gather(
        *(probe(s["name"], s["connection"]) for s in selected)
    )
    legacy = json.loads(Path("/home/joe/.lmstudio/mcp.json").read_text())["mcpServers"]
    results.append(
        await probe(
            "Legacy Context7 OAuth endpoint, without native OAuth credentials",
            {"type": "streamableHttp", "url": legacy["context7"]["url"]},
        )
    )
    launch = json.loads((ROOT / "state/bionic-native-launch.json").read_text())
    alive = (Path("/proc") / str(launch["pid"])).exists()
    lines = (
        (ROOT / "logs/bionic-native-launch.log")
        .read_text(errors="replace")
        .splitlines()
    )
    observations = []
    if any(
        "Failed to connect MCP server 'Atlassian'" in s
        and "Authentication required" in s
        for s in lines
    ):
        observations.append(
            "Native Bionic launch reports Atlassian MCP authentication required. This does not establish that it blocks core tools."
        )
    if any("Ignoring MCP tool" in s and "already used" in s for s in lines):
        observations.append(
            "Native Bionic launch reports duplicate GitHub tool names ignored; core execution impact unverified."
        )
    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "initiator": "Codex",
        "bionic_version": json.loads(
            Path("/opt/Bionic/resources/app/package.json").read_text()
        )["version"],
        "bionic_process_running": alive,
        "desktop_control": json.loads(
            (ROOT / "evidence/bionic-ui-surfaces.json").read_text()
        ),
        "mcp_diagnostics": results,
        "native_log_observations": observations,
        "bionic_run_acceptance": {
            "status": "BLOCKED",
            "outputs": None,
            "exit_codes": None,
            "reason": "No desktop UI control or documented native agent submission interface exposed to Codex. Operator must submit handoff/BIONIC_NATIVE_TASK.txt in an Allow coding project. No native acceptance command has been submitted.",
        },
        "codex_model_repair": json.loads(
            (ROOT / "evidence/bionic-launch-inference-repair.json").read_text()
        )
        if (ROOT / "evidence/bionic-launch-inference-repair.json").exists()
        else None,
        "limitations": [
            "Codex protocol probes do not verify Bionic approvals or native tool calls.",
            "Unauthenticated legacy OAuth endpoint probe does not verify Bionic stored OAuth credentials.",
            "No connector disabled, credential modified, approval bypassed, or security control changed.",
        ],
        "evidence": {
            "launch_log": "logs/bionic-native-launch.log",
            "fixture_setup": "state/bionic-native-case.json",
            "native_task": "handoff/BIONIC_NATIVE_TASK.txt",
        },
    }
    (ROOT / "evidence/bionic-native-diagnostics.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    (ROOT / "reports/BIONIC_NATIVE_DIAGNOSIS.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(json.dumps(report, indent=2))
    return 2


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
