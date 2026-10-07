import hashlib
import json
import os
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
start = time.perf_counter()
# Bounded pattern checks exercise RAM and filesystem, not a full hardware stress test.
pattern = bytes(range(256))
buffer = bytearray(pattern * (64 * 1024 * 1024 // 256))
assert len(buffer) == 64 * 1024 * 1024
for offset in range(0, len(buffer), 4096):
    assert buffer[offset : offset + 256] == pattern
expected = hashlib.sha256(buffer).hexdigest()
with tempfile.TemporaryDirectory(prefix="hardware-probe-", dir=ROOT / "scratch") as d:
    p = Path(d) / "pattern.bin"
    with p.open("wb") as f:
        f.write(buffer)
        f.flush()
        os.fsync(f.fileno())
    with p.open("rb") as f:
        actual = hashlib.file_digest(f, "sha256").hexdigest()
    assert actual == expected
cpu = sum(i * i for i in range(1, 1000001))
assert cpu == 333333833333500000
r = {
    "status": "PASS",
    "ram_bytes_exercised": len(buffer),
    "filesystem_sha256": actual,
    "cpu_sum_squares_1000000": cpu,
    "runtime_s": time.perf_counter() - start,
    "limitations": "Bounded single-process correctness test; does not replace memtest, storage SMART or long thermal stress.",
}
(ROOT / "evidence/hardware-validation.json").write_text(json.dumps(r, indent=2) + "\n")
print(json.dumps(r, indent=2))
