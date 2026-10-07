const fs = require('fs');
const { LMStudioClient } = require('../tools/lmstudio-client/node_modules/@lmstudio/sdk/dist/index.cjs');
(async () => {
  const context = Number(process.argv[2] || 32768);
  if (![16384, 32768, 49152, 65536].includes(context)) throw Error('Unsupported commissioning context');
  const client = new LMStudioClient({
    apiToken: fs.readFileSync('/home/joe/.lmstudio/credentials/local-work-api.token', 'utf8').trim()
  });
  for (const model of await client.llm.listLoaded()) {
    const info = await model.getModelInfo();
    if (!info.path?.includes('qwen3.8-27b')) throw Error('Unexpected loaded model; manual review required');
    if (info.quantization?.name === 'Q6_K' && info.contextLength === context) {
      console.log(JSON.stringify({ identifier: info.identifier, contextLength: info.contextLength, quantization: info.quantization.name }));
      return;
    }
    if (!process.argv.includes('--reconfigure')) throw Error('Loaded context/variant differs. Confirm model is idle, then explicitly use --reconfigure.');
    await client.llm.unload(info.identifier);
  }
  const model = await client.llm.load('qwen/qwen3.8-27b@q6_k', {
    identifier: 'qwen/qwen3.8-27b', verbose: false,
    config: { contextLength: context, gpu: { ratio: 1 }, maxParallelPredictions: 1,
      flashAttention: true, llamaKCacheQuantizationType: 'q8_0',
      llamaVCacheQuantizationType: 'q8_0', evalBatchSize: 1024 }
  });
  const info = await model.getModelInfo();
  console.log(JSON.stringify({ identifier: info.identifier, contextLength: info.contextLength,
    quantization: info.quantization?.name, sizeBytes: info.sizeBytes }));
})().catch(error => { console.error(error.message); process.exit(1); });
