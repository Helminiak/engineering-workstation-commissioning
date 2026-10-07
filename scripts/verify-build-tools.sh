#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
mkdir -p artifacts/build-tools
cmake -S tests -B artifacts/build-tools/cmake -G Ninja
cmake --build artifacts/build-tools/cmake
ctest --test-dir artifacts/build-tools/cmake --output-on-failure
clang++ -std=c++20 -Wall -Wextra -Werror -g tests/sum_squares.cpp -o artifacts/build-tools/clang-test
artifacts/build-tools/clang-test
clang++ --analyze -std=c++20 tests/sum_squares.cpp -o artifacts/build-tools/analysis.plist
valgrind --error-exitcode=1 --leak-check=full artifacts/build-tools/clang-test
gdb -batch -ex 'set disable-randomization off' -ex run --args artifacts/build-tools/clang-test
ccache g++ -std=c++20 tests/sum_squares.cpp -o artifacts/build-tools/cached-test
artifacts/build-tools/cached-test
rustfmt --check tests/sum_squares.rs
clippy-driver --test tests/sum_squares.rs -D warnings -o artifacts/build-tools/rust-clippy-test
artifacts/build-tools/rust-clippy-test
mvn -B -ntp -f tests/java-mbo/pom.xml package
java -ea -cp artifacts/java-mbo/maven/classes commissioning.OrderBookTest
hyperfine --warmup 1 --runs 3 --export-json evidence/compiled-benchmark.json artifacts/build-tools/clang-test
