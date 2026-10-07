#!/usr/bin/env bash
set -euo pipefail
# Run only after Joe explicitly approves the sudo batch. Not called automatically.
packages=(build-essential clang llvm cmake ninja-build gdb valgrind ccache openjdk-25-jdk maven rustc cargo rustfmt rust-clippy shellcheck hyperfine tmux htop tree nvtop lm-sensors pipx)
if [[ ${1:-} != --operator-approved ]]; then
  echo 'Operator approval required for sudo installation. Read evidence/development-install-simulation.txt.'
  exit 2
fi
cd /home/joe/LLM-Workspace
python3 scripts/commission.py checkpoint 'Operator-approved system package installation starting'
sudo apt-get install "${packages[@]}"
python3 scripts/commission.py checkpoint 'Approved apt operation finished; verify tools before marking PASS'
