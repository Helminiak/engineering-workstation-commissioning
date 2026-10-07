import asyncio
import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

ROOT = Path(__file__).resolve().parent.parent


async def main():
    result = {}
    # Independent optional connector sessions cannot prevent core tool initialization.
    for name, url in [
        ("context7-public", "https://mcp.context7.com/mcp"),
        ("simulated-broken-optional", "http://127.0.0.1:1/mcp"),
    ]:
        try:
            async with asyncio.timeout(20):
                async with streamable_http_client(url) as streams:  # noqa: SIM117 -- explicit MCP transport/session lifecycle boundaries
                    async with ClientSession(streams[0], streams[1]) as client:
                        await client.initialize()
                        tools = await client.list_tools()
                        result[name] = {
                            "status": "PASS",
                            "tools": [t.name for t in tools.tools],
                        }
        except Exception as e:  # noqa: BLE001 -- convert subsystem failures to recorded status
            result[name] = {"status": "FAIL", "exception_type": type(e).__name__}
    params = StdioServerParameters(
        command=str(ROOT / ".venv/bin/python"),
        args=[str(ROOT / "tools/workbench_mcp.py")],
    )
    async with stdio_client(params) as streams:  # noqa: SIM117 -- explicit MCP transport/session lifecycle boundaries
        async with ClientSession(*streams) as client:
            await client.initialize()
            res = await client.call_tool(
                "run_command", {"command": "scripts/local-agent-capability-test.sh"}
            )
            dump = res.model_dump(mode="json")
            result["core-after-failure"] = dump
            assert not res.is_error
            # Server structured tool payload and text content both retain command exit status.
            assert "PASS: shell/filesystem" in json.dumps(dump)
    assert result["simulated-broken-optional"]["status"] == "FAIL"
    (ROOT / "evidence/mcp-isolation.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
