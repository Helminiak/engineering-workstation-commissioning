import hashlib
import json
import resource
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from commissioning_streaming_forensics import analyze_stream

p = ROOT / "datasets/synthetic-large-forensic.jsonl"
n = 200000
with p.open("w") as f:

    def event(i):
        return {
            "sequence": i,
            "reference_ms": 1e12 + i * 1000,
            "source_ms": 1e12 + i * 1000 + 7 + i * 2,
            "value": i % 17,
        }

    for i in range(1, n + 1):
        if i == 12345:
            continue
        if i == 50000:
            f.write(json.dumps(event(i)) + "\n")
        if i == 100000:
            continue
        f.write(json.dumps(event(i)) + "\n")
        if i == 100001:
            f.write(json.dumps(event(100000)) + "\n")
original = hashlib.file_digest(p.open("rb"), "sha256").hexdigest()
report = analyze_stream(p)
assert report["sha256"] == original and report["records"] == n
assert report["duplicate_groups"] == 1 and report["duplicates"] == [(50000, 2)]
assert report["missing_count"] == 1 and report["missing_ranges"] == [[12345, 12345]]
assert len(report["out_of_order_positions"]) == 1
assert abs(report["clock_drift_ratio"] - 0.002) < 1e-10, report
assert hashlib.file_digest(p.open("rb"), "sha256").hexdigest() == original
report["status"] = "PASS"
report["max_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
report["proc_vm_hwm_kib"] = int(
    next(
        line.split()[1]
        for line in Path("/proc/self/status").read_text().splitlines()
        if line.startswith("VmHWM:")
    )
)
(ROOT / "evidence/streaming-forensics.json").write_text(
    json.dumps(report, indent=2) + "\n"
)
print(json.dumps(report, indent=2))
