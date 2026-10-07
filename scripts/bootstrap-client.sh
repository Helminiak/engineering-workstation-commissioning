#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
if [[ -f tools/lmstudio-client/node_modules/@lmstudio/sdk/dist/index.cjs ]]; then
 echo 'Existing SDK retained; inspect configs/lmstudio-client.package-lock.json for recorded version.'
 exit 0
fi
mkdir -p tools/lmstudio-client
cp configs/lmstudio-client.package.json tools/lmstudio-client/package.json
cp configs/lmstudio-client.package-lock.json tools/lmstudio-client/package-lock.json
npm ci --prefix tools/lmstudio-client
