// Read-only tokenizer measurements using an already loaded model, never autoload.
const fs = require('fs');
const crypto = require('crypto');
const cp = require('child_process');
const { LMStudioClient } = require('../tools/lmstudio-client/node_modules/@lmstudio/sdk/dist/index.cjs');

(async () => {
  const client = new LMStudioClient({apiToken: fs.readFileSync('/home/joe/.lmstudio/credentials/local-work-api.token', 'utf8').trim()});
  const handles = await client.llm.listLoaded();
  if (handles.length !== 1) throw new Error('Expected exactly one already loaded model');
  const model = handles[0];
  const info = await model.getModelInfo();
  const config = await model.getLoadConfig();
  fs.writeFileSync('evidence/bionic-post-reboot-loaded-model.json', JSON.stringify({timestamp: new Date().toISOString(), info, config}, null, 2) + '\n', {mode:0o600});
  const measurement = JSON.parse(fs.readFileSync('evidence/bionic-mcp-payload-measurement.json', 'utf8'));
  const rows = [];
  for (const provider of measurement.providers.filter(x => x.status === 'PASS')) {
    const raw = JSON.parse(fs.readFileSync(provider.raw_evidence, 'utf8'));
    const largest = [...raw.tools].sort((a,b) => JSON.stringify(b.inputSchema).length - JSON.stringify(a.inputSchema).length)[0];
    const [functions, instructions, largestSchema] = await model.tokenize([
      raw.model_facing_json, raw.instructions, JSON.stringify(largest.inputSchema)
    ]);
    rows.push({provider:provider.provider, tool_count:provider.tool_count,
      compact_function_json_tokens:functions.length, instructions_tokens:instructions.length,
      largest_input_schema:{name:largest.name, tokens:largestSchema.length}});
  }
  const all = measurement.providers.filter(x=>x.status==='PASS').flatMap(x=>JSON.parse(JSON.parse(fs.readFileSync(x.raw_evidence,'utf8')).model_facing_json));
  const combinedTokens = await model.countTokens(JSON.stringify(all));
  const catalogs = measurement.providers.filter(x=>x.status==='PASS').map(x=>({provider:x.provider,
    tools:JSON.parse(JSON.parse(fs.readFileSync(x.raw_evidence,'utf8')).model_facing_json)}));
  const replays = [];
  for (const [label, defs] of [
    ['hello_no_tools', []],
    ['hello_all_measured_mcp_catalogs', all],
    ['hello_measured_catalogs_without_notion', catalogs.filter(x=>x.provider!=='Notion').flatMap(x=>x.tools)],
    ['hello_local_workbench_catalog_only', catalogs.find(x=>x.provider==='Local Workbench').tools]
  ]) {
    const prompt = await model.applyPromptTemplate([{role:'user',content:'hello'}], {toolDefinitions:defs});
    replays.push({label, tools:defs.length, formatted_prompt_tokens:await model.countTokens(prompt),
      formatted_prompt_characters:prompt.length});
  }
  const template = config.promptTemplate?.jinjaPromptTemplate?.template || '';
  const result = {timestamp:new Date().toISOString(), catalog_timestamp:measurement.timestamp,
    initiator:'Codex read-only loaded-model tokenizer; no generation or native submission',
    model:{identifier:info.identifier,quantization:info.quantization?.name,context_length:info.contextLength,
      max_parallel_predictions:config.maxParallelPredictions,gpu:config.gpu,
      unified_kv_cache:config.useUnifiedKvCache,offload_kv_cache_to_gpu:config.offloadKVCacheToGpu,
      k_cache_quantization:config.llamaKCacheQuantizationType,v_cache_quantization:config.llamaVCacheQuantizationType,
      template_sha256:crypto.createHash('sha256').update(template).digest('hex'),
      template_inlines_each_tool_json:template.includes('tool | tojson')},
    gpu_csv:cp.execFileSync('nvidia-smi',['--query-gpu=memory.total,memory.used,memory.free','--format=csv,noheader,nounits'],{encoding:'utf8'}).trim(),
    providers:rows, combined_compact_function_json_tokens:combinedTokens,
    synthetic_template_measurements:replays,
    limits:['Measured current catalog text, not the complete native request.',
      'Bionic filtering/name rewriting, native modules, template JSON formatting and session context are additional factors.',
      'Per-component token counts do not exactly add to complete chat counts.',
      'Synthetic hello template measurements do not submit a GUI request or execute tools; native Bionic module/system content is absent.']};
  fs.writeFileSync('evidence/bionic-post-reboot-payload-tokens.json', JSON.stringify(result,null,2)+'\n',{mode:0o600});
  console.log(JSON.stringify(result,null,2));
})().catch(() => { console.error('Read-only tokenizer measurement failed; no settings changed.'); process.exitCode=1; });
