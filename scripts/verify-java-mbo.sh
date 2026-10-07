#!/usr/bin/env bash
set -euo pipefail
cd /home/joe/LLM-Workspace
mkdir -p artifacts/java-mbo/classes
javac -Xlint:all -Werror -d artifacts/java-mbo/classes tests/java-mbo/src/main/java/commissioning/*.java
java -Xmx256m -ea -cp artifacts/java-mbo/classes commissioning.OrderBookTest
