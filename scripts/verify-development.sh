#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
mkdir -p artifacts/development
for program in g++ java javac mvn rustc cargo shellcheck; do
 command -v "$program" >/dev/null || { echo "Missing: $program"; exit 2; }
done
g++ -std=c++20 -Wall -Wextra -Werror tests/sum_squares.cpp -o artifacts/development/cpp-test
artifacts/development/cpp-test
javac -d artifacts/development tests/SumSquares.java
java -cp artifacts/development SumSquares
rustc --test tests/sum_squares.rs -o artifacts/development/rust-test
artifacts/development/rust-test
rustc tests/sum_squares.rs -o artifacts/development/rust-main
artifacts/development/rust-main
shellcheck scripts/*.sh
scripts/local-agent-capability-test.sh
