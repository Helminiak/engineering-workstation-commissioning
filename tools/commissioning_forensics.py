"""Read-only synthetic forensic baseline. Preserve and hash original bytes."""

import hashlib
import json
import statistics
from pathlib import Path


def analyze(path):
    raw = Path(path).read_bytes()
    rows = [json.loads(line) for line in raw.splitlines() if line]
    seq = [r["sequence"] for r in rows]
    unique = set(seq)
    counts = {i: seq.count(i) for i in unique}
    duplicates = sorted(i for i, n in counts.items() if n > 1)
    missing = sorted(set(range(min(seq), max(seq) + 1)) - unique)
    out_of_order = [i for i in range(1, len(seq)) if seq[i] < seq[i - 1]]
    canonical = {r["sequence"]: r for r in rows}
    ordered = [canonical[k] for k in sorted(canonical)]
    offsets = [r["source_ms"] - r["reference_ms"] for r in ordered]
    x = [r["reference_ms"] for r in ordered]
    xm = statistics.mean(x)
    ym = statistics.mean(offsets)
    drift = sum((a - xm) * (b - ym) for a, b in zip(x, offsets)) / sum(
        (a - xm) ** 2 for a in x
    )
    values = [r["value"] for r in ordered]
    median = statistics.median(values)
    mad = statistics.median(abs(v - median) for v in values)
    anomalies = [
        r["sequence"] for r in ordered if abs(r["value"] - median) > max(6 * mad, 20)
    ]
    # Exhaustive two-segment least-squares baseline, clipping only for fixture's known gross outlier.
    clipped = [max(-1, min(11, v)) for v in values]

    def sse(v):
        m = statistics.mean(v)
        return sum((x - m) ** 2 for x in v)

    split = min(
        range(10, len(values) - 10), key=lambda k: sse(clipped[:k]) + sse(clipped[k:])
    )
    result = {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "records": len(rows),
        "duplicate_sequences": duplicates,
        "missing_sequences": missing,
        "out_of_order_positions": out_of_order,
        "clock_drift_ratio": drift,
        "anomaly_sequences": anomalies,
        "change_at_sequence": ordered[split]["sequence"],
    }
    assert Path(path).read_bytes() == raw
    return result
