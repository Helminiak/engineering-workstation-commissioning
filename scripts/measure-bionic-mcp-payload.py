#!/usr/bin/env python3
"""Read enabled MCP tool catalogs without calling tools or changing app settings.

Uses existing authentication only, never refreshes credentials. Raw catalogs stay
owner-only and Git-ignored. This is a catalog measurement, not a native request.
"""
import asyncio
import datetime
import hashlib
import json
import os
import re
from pathlib import Path

import httpx2
from mcp import ClientSession, StdioServerParameters
from mcp.types import PaginatedRequestParams
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

ROOT = Path(__file__).resolve().parent.parent
CONFIG = Path('/home/joe/.lmstudio/apps/bionic/.internal/ng-mcp.json')


def error_metadata(exc):
    result = [{'type': type(exc).__name__}]
    status = getattr(getattr(exc, 'response', None), 'status_code', None)
    if status:
        result[0]['http_status'] = status
    if isinstance(exc, AttributeError):
        match = re.search(r"has no attribute '([A-Za-z_][A-Za-z_0-9]*)'", str(exc))
        if match:
            result[0]['missing_attribute'] = match[1]
    if isinstance(exc, TypeError):
        match = re.search(r"unexpected keyword argument '([A-Za-z_][A-Za-z_0-9]*)'", str(exc))
        if match:
            result[0]['unexpected_keyword'] = match[1]
    for child in getattr(exc, 'exceptions', ()):
        result.extend(error_metadata(child))
    return result


async def catalog(client, name):
    init = await client.initialize()
    tools = []
    cursor = None
    for _ in range(100):
        page = await client.list_tools(params=PaginatedRequestParams(cursor=cursor) if cursor else None)
        tools.extend(t.model_dump(mode='json', exclude_none=True, by_alias=True) for t in page.tools)
        cursor = page.next_cursor
        if not cursor:
            break
    else:
        raise RuntimeError('pagination_limit')
    instructions = init.instructions or ''
    facing = [{'type': 'function', 'function': {'name': t['name'],
               'description': t.get('description', ''),
               'parameters': t['inputSchema']}} for t in tools]
    serialized = json.dumps(facing, ensure_ascii=False, separators=(',', ':'))
    return ({'provider': name, 'status': 'PASS', 'tool_count': len(tools),
            'function_json_characters': len(serialized),
            'instructions_characters': len(instructions),
            'function_json_sha256': hashlib.sha256(serialized.encode()).hexdigest(),
            'largest_tools': sorted([{'name': t['name'],
                'description_characters': len(t.get('description', '')),
                'input_schema_characters': len(json.dumps(t['inputSchema'], ensure_ascii=False, separators=(',', ':')))}
                for t in tools], key=lambda t: t['description_characters'] + t['input_schema_characters'], reverse=True)[:5]},
            {'tools': tools, 'model_facing_json': serialized, 'instructions': instructions})


async def probe(server, raw_dir):
    name, conn = server['name'], server['connection']
    try:
        async with asyncio.timeout(40):
            if conn['type'] == 'stdio':
                # Run installed cached entry points directly; never npx/install/fetch.
                cached = {
                    'Workspace Files': ('/home/joe/.npm/_npx/a3241bba59c344f5/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js', ['/home/joe/LLM-Workspace']),
                    'Playwright Browser': ('/home/joe/.npm/_npx/9833c18b2d85bc59/node_modules/@playwright/mcp/cli.js', conn.get('args', [])[2:]),
                }
                command, args = conn['command'], conn.get('args', [])
                if name in cached:
                    entry, flags = cached[name]
                    if not Path(entry).is_file():
                        return {'provider': name, 'status': 'NOT_TESTED', 'reason': 'cached entry point missing; npx skipped'}
                    command = '/home/joe/.local/share/nodejs/node-v22.23.3-linux-x64/bin/node'
                    args = [entry, *flags]
                elif name != 'Local Workbench':
                    return {'provider': name, 'status': 'NOT_TESTED', 'reason': 'unrecognized executable; launch skipped'}
                params = StdioServerParameters(command=command, args=args,
                    env=conn.get('env') or None, cwd=conn.get('cwd') or str(ROOT))
                async with stdio_client(params) as streams, ClientSession(*streams) as client:
                    row, raw = await catalog(client, name)
            else:
                headers = dict(conn.get('headers') or {})
                auth = conn.get('auth') or {}
                if auth.get('type') == 'bearerToken':
                    headers['Authorization'] = 'Bearer ' + auth['token']
                elif auth.get('type') == 'oauth':
                    p = Path('/home/joe/.lmstudio/credentials/ng-mcp-oauth') / server['id'] / 'tokens.json'
                    if not p.exists():
                        return {'provider': name, 'status': 'NOT_TESTED', 'reason': 'no existing OAuth token; no login/refresh attempted'}
                    headers['Authorization'] = 'Bearer ' + json.loads(p.read_text())['tokens']['access_token']
                async with httpx2.AsyncClient(headers=headers, timeout=30) as http:
                    async with streamable_http_client(conn['url'], http_client=http) as streams, ClientSession(streams[0], streams[1]) as client:
                        row, raw = await catalog(client, name)
            target = raw_dir / (server['id'] + '.json')
            target.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + '\n')
            target.chmod(0o600)
            row['raw_evidence'] = str(target.relative_to(ROOT))
            if conn['type'] == 'stdio' and name != 'Local Workbench':
                row['source_note'] = 'Installed cached CLI; configured npx command not invoked and no package fetched'
            return row
    except Exception as exc:
        # Never print exception messages, URLs, headers, tokens or tracebacks.
        return {'provider': name, 'status': 'UNAVAILABLE', 'errors': error_metadata(exc)}


async def main():
    os.umask(0o077)
    now = datetime.datetime.now(datetime.timezone.utc)
    raw_dir = ROOT / 'evidence' / ('bionic-mcp-catalog-' + now.strftime('%Y%m%dT%H%M%SZ'))
    raw_dir.mkdir(mode=0o700)
    servers = [s for s in json.loads(CONFIG.read_text())['servers'] if s.get('enabled')]
    rows = await asyncio.gather(*(probe(s, raw_dir) for s in servers))
    report = {'timestamp': now.isoformat(), 'initiator': 'Codex read-only MCP catalog probes',
              'scope': 'initialize/list_tools only; no tool calls, credential refresh, app settings or model changes',
              'providers': rows,
              'limitations': ['Catalog character counts are not Qwen token counts.',
                  'Fresh catalogs do not establish the exact historical or GUI-assembled request.',
                  'Bionic name rewriting, filtering, native tools, project context and chat template remain unmeasured.']}
    (ROOT / 'evidence/bionic-mcp-payload-measurement.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'timestamp': report['timestamp'], 'providers': [
        {k: row[k] for k in ('provider', 'status', 'tool_count', 'function_json_characters', 'instructions_characters', 'errors') if k in row}
        for row in rows]}, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
