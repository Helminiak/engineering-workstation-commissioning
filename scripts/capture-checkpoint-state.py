#!/usr/bin/env python3
"""Read-only, whitelisted host inventory for a final checkpoint. Never read clipboard."""
import datetime
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def command(argv, timeout=20):
    p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=timeout, check=False)
    return {'exit_code': p.returncode, 'stdout': p.stdout.strip()}


def main():
    os.umask(0o077)
    now = datetime.datetime.now(datetime.timezone.utc)
    processes = command(['ps', '-eo', 'pid,ppid,comm'])
    models = command(['node', 'scripts/model-info.cjs'])
    loaded = []
    if models['exit_code'] == 0:
        for row in json.loads(models['stdout']):
            cfg = row['config']
            loaded.append({'identifier':row['identifier'], 'quantization':row['quantization'],
                'context_length':row['contextLength'], 'parallel_slots':cfg.get('maxParallelPredictions'),
                'gpu':cfg.get('gpu'), 'kv_offload':cfg.get('offloadKVCacheToGpu'),
                'k_cache_quantization':cfg.get('llamaKCacheQuantizationType'),
                'v_cache_quantization':cfg.get('llamaVCacheQuantizationType')})
    versions = {name:command(argv) for name,argv in {
        'python_system':['python3','--version'], 'python_local_agent':['.venv/bin/python','--version'],
        'python_quant':['venvs/quant/bin/python','--version'], 'python_gpu':['venvs/gpu/bin/python','--version'],
        'node':['node','--version'], 'npm':['npm','--version'], 'npx':['npx','--version'],
        'git':['git','--version'], 'github_cli':['gh','--version'], 'lms_cli':['lms','--version'],
        'uv':['uv','--version'], 'rust':['rustc','--version'], 'gcc':['gcc','-dumpfullversion'],
        'clipboard_package':['dpkg-query','-W','-f=${Status} ${Version}\n','wl-clipboard']}.items()}
    apps = {}
    for name, path in [('bionic','/opt/Bionic/resources/app/package.json'), ('lmstudio','/opt/LM-Studio/resources/app/package.json')]:
        p = Path(path)
        apps[name] = json.loads(p.read_text()).get('version') if p.exists() else 'MISSING'
    git = {'commit':command(['git','rev-parse','HEAD'])['stdout'],
           'branch':command(['git','branch','--show-current'])['stdout'],
           'worktree':command(['git','status','--short'])['stdout']}
    # Remote allowlist check only; never emit a credential-bearing remote URL.
    remote = command(['git','remote','get-url','origin'])['stdout']
    git['authorized_remote_matches'] = remote in (
        'https://github.com/Helminiak/engineering-workstation-commissioning.git',
        'https://github.com/Helminiak/engineering-workstation-commissioning',
        'git@github.com:Helminiak/engineering-workstation-commissioning.git')
    git['repository'] = 'https://github.com/Helminiak/engineering-workstation-commissioning'
    result = {'timestamp':now.isoformat(), 'operator_directive':'STOP_NEW_WORK; checkpoint only',
        'kernel':command(['uname','-r'])['stdout'], 'boot_time':command(['uptime','-s'])['stdout'],
        'gpu':command(['nvidia-smi','--query-gpu=name,driver_version,memory.total,memory.used,memory.free','--format=csv,noheader']),
        'loaded_models':loaded, 'versions':versions, 'app_versions':apps,
        'processes_without_arguments':processes, 'loopback_listeners':command(['ss','-ltnp']), 'git':git}
    target = ROOT/'evidence'/('checkpoint-host-'+now.strftime('%Y%m%dT%H%M%SZ')+'.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'state/final-checkpoint-host.json').write_text(json.dumps({'evidence':str(target.relative_to(ROOT)), 'timestamp':now.isoformat()},indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['timestamp','gpu','loaded_models','app_versions','git']},indent=2))


if __name__ == '__main__':
    main()
