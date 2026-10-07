#!/usr/bin/env python3
"""Evidence-driven stage runner. Explicit verification commands; no implicit PASS."""
import argparse,datetime,json,os,subprocess,tempfile,fcntl,signal
from pathlib import Path
ROOT=Path(os.environ.get('COMMISSION_ROOT',Path(__file__).resolve().parent.parent))
C=ROOT/'commissioning'
STATES=['NOT_STARTED','IN_PROGRESS','PASS','PASS_WITH_LIMITATIONS','FAIL','BLOCKED','MANUAL_REQUIRED']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def atomic(path,obj):
 fd,name=tempfile.mkstemp(dir=path.parent)
 with os.fdopen(fd,'w') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(name,path)
def checkpoint(p,note):
 p['updated_at']=now();atomic(C/'progress.json',p)
 done=[k for k,v in p['stages'].items() if v['status'] in ('PASS','PASS_WITH_LIMITATIONS')]
 pending=[k for k,v in p['stages'].items() if v['status'] not in ('PASS','PASS_WITH_LIMITATIONS')]
 commit=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True).stdout.strip() or 'not committed'
 rows='\n'.join(f"- {k}: {v['status']}" for k,v in p['stages'].items())
 (C/'STATUS.md').write_text(f'# Status\nCheckpoint: {p["updated_at"]}\n{note}\n\n{rows}\n')
 (C/'TASKS.md').write_text('# Tasks\n\n'+rows+'\n\nNext unfinished: '+(pending[0] if pending else 'none')+'\n')
 with (C/'CHANGELOG.md').open('a') as f:f.write(f'\n- {now()}: {note}\n')
 issues=json.loads((C/'open_issues.json').read_text()).get('issues',[])
 text=f'''# Resume commissioning
Objective: verified engineering workstation; execution and handoff before package expansion.
Checkpoint: {p['updated_at']}
Verified phases: {', '.join(done) or 'none'}
Unfinished phases: {', '.join(pending)}
Stage status:\n{rows}
Open issues: {json.dumps(issues)}
Current commit before this checkpoint: {commit}. Run git log -1 for latest committed state.
Currently running: no managed background jobs; IN_PROGRESS may reflect an interrupted runner, reverify it.
First command: scripts/show_status.sh
Next: inspect evidence for {pending[0] if pending else 'end_to_end'}; rerun recorded verifier before continuing.
Reproduce: python3 scripts/commission.py verify STAGE --command 'VERIFIER' (inspect progress.json commands).
Do not repeat: working NVIDIA driver, working Node, existing model downloads; do not replace existing integrations.
Approvals required: sudo/system/security changes; new GitHub repository; merge/force push/deploy.
Raw stdout/stderr/exit codes: evidence/*.json; tests: tests/; logs: logs/. Raw logs excluded from Git.
Local bridge runs with Joe's full account privileges; workspace cwd is not a security sandbox.
No credentials in Git. No production branch changes. No external uploads of private data.
'''
 (C/'NEXT_AGENT.md').write_text(text)
 for name in ['CODEX_RESUME.md','LOCAL_LLM_START_HERE.md']:(ROOT/'handoff'/name).write_text(text)
def main():
 ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='action',required=True)
 sub.add_parser('status'); cp=sub.add_parser('checkpoint');cp.add_argument('note')
 v=sub.add_parser('verify');v.add_argument('stage');v.add_argument('--command',required=True);v.add_argument('--timeout',type=int,default=180);v.add_argument('--limitations',default='')
 s=sub.add_parser('set');s.add_argument('stage');s.add_argument('status',choices=STATES);s.add_argument('reason')
 a=ap.parse_args()
 with (C/'.runner.lock').open('w') as lock:
  if a.action!='status':fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  p=json.loads((C/'progress.json').read_text())
  if a.action=='status':
   for k,v in p['stages'].items():print(k,v['status'])
   print('Checkpoint:',p['updated_at']);print('Issues:',(C/'open_issues.json').read_text());return
  if a.action=='checkpoint':checkpoint(p,a.note);return
  st=p['stages'][a.stage]
  if a.action=='set':st['status']=a.status;st['remaining_issues']=[a.reason];checkpoint(p,f'{a.stage}: {a.status}: {a.reason}');return
  st['status']='IN_PROGRESS';st['start_time']=now();checkpoint(p,f'{a.stage}: verification started')
  record={'stage':a.stage,'start_time':now(),'command':a.command}
  q=subprocess.Popen(['/bin/bash','-c',a.command],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
  try:
   stdout,stderr=q.communicate(timeout=a.timeout)
   record.update(exit_code=q.returncode,stdout=stdout,stderr=stderr)
  except subprocess.TimeoutExpired:
   os.killpg(q.pid,signal.SIGTERM)
   try:stdout,stderr=q.communicate(timeout=2)
   except subprocess.TimeoutExpired:
    os.killpg(q.pid,signal.SIGKILL);stdout,stderr=q.communicate()
   record.update(exit_code=124,stdout=stdout,stderr=stderr+'\nVerification timeout; process group terminated')
  record['end_time']=now();ep=ROOT/'evidence'/f'{a.stage}-{datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")}.json';atomic(ep,record)
  st['commands'].append({k:record[k] for k in ['command','exit_code','start_time','end_time']});st['evidence'].append(str(ep.relative_to(ROOT)))
  st['end_time']=now();st['verification']=record['exit_code']==0
  st['status']=('PASS_WITH_LIMITATIONS' if a.limitations else 'PASS') if record['exit_code']==0 else 'FAIL'
  st['remaining_issues']=[a.limitations] if a.limitations else ([] if record['exit_code']==0 else ['Verifier failed; inspect evidence and persist distinct repair attempts.'])
  checkpoint(p,f'{a.stage}: {st["status"]}');print(record['stdout']);print(record['stderr']);raise SystemExit(0 if record['exit_code']==0 else 1)
if __name__=='__main__':main()
