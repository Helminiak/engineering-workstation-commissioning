#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
git status --short --branch
git log -1 --format='%h %s'
git remote -v
