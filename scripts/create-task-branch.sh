#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
name=${1:?Supply task name}
[[ "$name" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ ]] || exit 2
test -z "$(git status --porcelain)" || { echo 'Commit or preserve current work first'; exit 1; }
git switch -c "task/$name"
