"""Local model drives actual MCP tools; independent artifact validation follows."""
import asyncio,json,subprocess,time,urllib.request,sys
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parent.parent
FIX=ROOT/'scratch/local-agent-acceptance'
async def main():
 FIX.mkdir(exist_ok=True)
 if not (FIX/'.git').exists():
  subprocess.run(['git','init','-q',str(FIX)],check=True)
  (FIX/'tracked.txt').write_text('baseline\n')
  subprocess.run(['git','-C',str(FIX),'add','tracked.txt'],check=True)
  subprocess.run(['git','-C',str(FIX),'-c','user.name=Acceptance Fixture','-c','user.email=fixture@localhost','commit','-qm','Baseline fixture'],check=True)
 token=Path('/home/joe/.lmstudio/credentials/local-work-api.token').read_text().strip()
 transcript=[]
 params=StdioServerParameters(command=str(ROOT/'.venv/bin/python'),args=[str(ROOT/'tools/workbench_mcp.py')])
 async with stdio_client(params) as (read,write):
  async with ClientSession(read,write) as session:
   await session.initialize();listed=await session.list_tools()
   tools=[{'type':'function','function':{'name':t.name,'description':t.description,'parameters':t.input_schema}} for t in listed.tools if t.name in ['run_command','run_python','read_document']]
   messages=[{'role':'system','content':'You are a local commissioning agent. Use tools to perform the task, execute actual commands and inspect results. Only modify scratch/local-agent-acceptance. No sudo, network, secrets, deployments or pushes. Be concise.'},{'role':'user','content':'''Acceptance test in /home/joe/LLM-Workspace/scratch/local-agent-acceptance. Independently perform all: execute whoami, pwd and nvidia-smi; create and read probe.txt containing verified; create and execute check.sh printing bash-ok; create calculate.py implementing sum_squares(n), summing i*i for i=1..n; create and run test_calculate.py asserting sum_squares(10)==385 and sum_squares(0)==0; inspect Git status; append commissioned to tracked.txt; show Git diff; execute Node and Python version checks; generate report.md containing actual exit codes and test results. Use run_command or run_python. Do not just describe commands. Finish with a concise result. /no_think'''}]
   for turn in range(24):
    payload={'model':'qwen/qwen3.8-27b','messages':messages,'tools':tools,'temperature':0.2,'max_tokens':6000,'reasoning_effort':'none'}
    req=urllib.request.Request('http://127.0.0.1:1234/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+token})
    start=time.monotonic()
    def request():
     with urllib.request.urlopen(req,timeout=180) as f:return json.load(f)
    response=await asyncio.to_thread(request)
    msg=response['choices'][0]['message'];messages.append(msg);transcript.append({'turn':turn,'seconds':time.monotonic()-start,'response':response})
    for call in msg.get('tool_calls') or []:
     name=call['function']['name'];args=json.loads(call['function']['arguments'])
     if name not in ['run_command','run_python','read_document']:raise ValueError('Unexpected tool')
     result=await session.call_tool(name,args);content=json.dumps(result.model_dump(mode='json'),default=str)
     messages.append({'role':'tool','tool_call_id':call['id'],'content':content});transcript.append({'tool':name,'arguments':args,'result':json.loads(content)})
     print('tool:',name,'result error:',result.is_error,flush=True)
    (ROOT/'evidence/local-llm-acceptance.json').write_text(json.dumps(transcript,indent=2)+'\n')
    if not msg.get('tool_calls'):
     print('Model final:',msg.get('content'));break
   else:raise RuntimeError('Tool turn limit reached')
 # Separate verifier does not depend on model report.
 required=['probe.txt','check.sh','calculate.py','test_calculate.py','report.md']
 for name in required:assert (FIX/name).is_file(),name
 assert 'verified' in (FIX/'probe.txt').read_text()
 assert 'commissioned' in (FIX/'tracked.txt').read_text()
 for command in [['bash','check.sh'],[sys.executable,'test_calculate.py']]:subprocess.run(command,cwd=FIX,check=True)
 diff=subprocess.check_output(['git','diff'],cwd=FIX,text=True);assert '+commissioned' in diff
 assert any(x.get('tool') for x in transcript),'No tool calls'
 all_commands='\n'.join(x.get('arguments',{}).get('command','') for x in transcript)
 for expected in ['whoami','pwd','nvidia-smi','git status','git diff']:assert expected in all_commands,expected
 print('PASS: independent artifact, Bash, Python test and Git diff verification')
if __name__=='__main__':asyncio.run(main())
