#!/usr/bin/env python3
"""Current load/VRAM and dated native errors; never change settings or infer PASS."""
import datetime
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_optional(path):
    target = ROOT / path
    return json.loads(target.read_text()) if target.exists() else None


def main():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    gpu = subprocess.run(['nvidia-smi', '--query-gpu=memory.total,memory.used,memory.free',
                          '--format=csv,noheader,nounits'], capture_output=True, text=True, check=False)
    vram = None
    if gpu.returncode == 0:
        total, used, free = map(int, gpu.stdout.strip().split(','))
        vram = {'total': total, 'used': used, 'free': free}
    model_query = subprocess.run(['node', 'scripts/model-info.cjs'], cwd=ROOT,
                                capture_output=True, text=True, timeout=20, check=False)
    loaded = []
    if model_query.returncode == 0:
        for model in json.loads(model_query.stdout):
            cfg = model['config']
            loaded.append({'identifier': model['identifier'], 'quantization': model['quantization'],
                           'context_length': model['contextLength'], 'parallel_slots': cfg.get('maxParallelPredictions'),
                           'gpu_offload_ratio': cfg.get('gpu', {}).get('ratio'),
                           'kv_offload': cfg.get('offloadKVCacheToGpu')})
    errors = []
    for logfile in sorted(Path('/home/joe/.lmstudio/apps/bionic/server-logs').rglob('*.log')):
        last_timestamp = None
        for line_number, line in enumerate(logfile.read_text(errors='replace').splitlines(), 1):
            stamp = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', line)
            if stamp:
                last_timestamp = stamp[1]
            match = re.search(r'request \((\d+) tokens\) exceeds the available context size \((\d+) tokens\)', line)
            if match:
                request, context = map(int, match.groups())
                errors.append({'source': str(logfile), 'line': line_number,
                               'timestamp_local': last_timestamp, 'request_tokens': request,
                               'available_context': context, 'excess_tokens': request-context})
    report = {'timestamp': now, 'current_usability': 'BLOCKED',
              'historical_native_acceptance': 'PASS; retained independently, not rerun',
              'actual_loaded_models': loaded, 'vram_mib': vram,
              'telemetry_status': 'PASS' if loaded and vram else 'INCOMPLETE',
              'latest_native_context_rejections': errors[-12:],
              'payload_measurement': read_optional('evidence/bionic-post-reboot-payload-tokens.json'),
              'backup': read_optional('state/bionic-context-loaded-backup.json'),
              'regular_gui_comparison': 'NOT_TESTED: no native GUI controls or identified regular GUI result',
              'reason': 'Native hello overflow recorded; no fresh successful native repair/retest established.',
              'freshness': 'Load/VRAM sampled now; each native error and catalog sample retains its own timestamp.',
              'changes': 'No model/context/plugin/security/driver changes. Current report writes only.',
              'next': 'Preserve controls/coding tools. Supported scoped schema experiment and native retest need UI control. Core API/MCP execution can be verified independently.'}
    (ROOT / 'reports/BIONIC_CONTEXT_DIAGNOSIS.json').write_text(json.dumps(report, indent=2)+'\n')
    (ROOT / 'reports/BIONIC_CONTEXT_DIAGNOSIS.md').write_text(
        '# Bionic current usability — BLOCKED\n\n'
        f'Telemetry captured {now}. Actual models: {json.dumps(loaded)}. '
        f'VRAM MiB: {json.dumps(vram)}.\n\n'
        'Native errors are dated observations; no fresh native success is established. '
        'Read [post-reboot payload diagnosis](BIONIC_CONTEXT_POST_REBOOT.md) for measured Notion overhead. '
        'Regular GUI comparison unverified; historical native acceptance retained. No settings changed.\n')
    print(json.dumps({'status':'BLOCKED', 'loaded':loaded, 'vram_mib':vram,
                      'latest_native_error':errors[-1] if errors else None}, indent=2))
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
