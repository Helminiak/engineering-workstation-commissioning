#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/joe/LLM-Workspace
cd "$ROOT"
printf 'user=%s\ncwd=%s\n' "$(whoami)" "$PWD"
test -r "$ROOT" && test -w "$ROOT" && test -x "$ROOT"
tmp=$(mktemp -d "$ROOT/scratch/capability.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
printf 'filesystem verified\n' > "$tmp/probe.txt"
test "$(cat "$tmp/probe.txt")" = 'filesystem verified'
printf '#!/usr/bin/env bash\nset -euo pipefail\nprintf "bash verified\\n"\n' > "$tmp/probe.sh"
bash "$tmp/probe.sh"
python3 -c 'assert sum(range(11)) == 55; print("python verified")'
node -e 'if ([1,2,3].reduce((a,b)=>a+b,0)!==6) process.exit(1); console.log("node verified")'
npm --version
npx --version
test "$(git -C "$ROOT" rev-parse --is-inside-work-tree)" = true
git -C "$ROOT" status --porcelain
printf 'PASS: shell/filesystem/Python/Node/npm/npx/Git/workspace permissions\n'
