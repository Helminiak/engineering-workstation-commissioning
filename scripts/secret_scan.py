#!/usr/bin/env python3
"""Local staged-content heuristic scan. Does not replace a full Gitleaks audit."""

import re
import subprocess
import sys

paths = (
    subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"]
    )
    .decode()
    .split("\0")
)
patterns = [
    r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
    r"\bghp_[A-Za-z0-9]{30,}",
    r"\bgithub_pat_[A-Za-z0-9_]{40,}",
    r"\bAKIA[A-Z0-9]{16}",
    r"\bsk-[A-Za-z0-9]{32,}",
    r"(?i)bearer\s+[A-Za-z0-9._-]{30,}",
]
failed = []
for p in filter(None, paths):
    content = subprocess.check_output(["git", "show", ":" + p]).decode(errors="replace")
    if any(re.search(x, content) for x in patterns):
        failed.append(p)
if failed:
    print("Potential secrets in:", ", ".join(failed))
    sys.exit(1)
print("PASS: staged-content heuristic scan; raw evidence remains excluded")
