import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from commissioning_forensics import analyze

p = ROOT / "datasets/synthetic-forensics.jsonl"
rows = []
for i in range(1, 101):
    if i == 31:
        continue
    rows.append(
        {
            "sequence": i,
            "reference_ms": i * 1000,
            "source_ms": i * 1000 + 7 + i * 2,
            "value": (0 if i <= 50 else 10)
            + (i % 3 - 1) * 0.01
            + (100 if i == 75 else 0),
        }
    )
rows.insert(20, dict(rows[19]))
rows[40], rows[41] = rows[41], rows[40]
raw = "".join(json.dumps(r) + "\n" for r in rows)
p.write_text(raw)
before = hashlib.sha256(p.read_bytes()).hexdigest()
start = time.perf_counter()
r = analyze(p)
assert r["duplicate_sequences"] == [20], r
assert r["missing_sequences"] == [31]
assert r["out_of_order_positions"]
assert abs(r["clock_drift_ratio"] - 0.002) < 1e-12
assert r["anomaly_sequences"] == [75]
assert r["change_at_sequence"] == 51
assert r["sha256"] == before
r["runtime_s"] = time.perf_counter() - start
r["status"] = "PASS"
(ROOT / "evidence/forensics-validation.json").write_text(json.dumps(r, indent=2) + "\n")
print(json.dumps(r, indent=2))
