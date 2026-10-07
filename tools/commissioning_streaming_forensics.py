"""Read-only JSONL forensic analysis with disk-backed ordering and bounded RAM."""

import hashlib
import json
import math
import sqlite3
import tempfile
import time
from pathlib import Path

ROOT = Path("/home/joe/LLM-Workspace")


def analyze_stream(path, limit=100):
    path = Path(path)
    before = path.stat()
    digest = hashlib.sha256()
    start = time.perf_counter()
    with tempfile.TemporaryDirectory(
        prefix="forensic-index-", dir=ROOT / "scratch"
    ) as temp:
        db = sqlite3.connect(Path(temp) / "events.sqlite")
        db.execute("pragma cache_size=-8192")
        db.execute("pragma temp_store=FILE")
        db.execute(
            "create table events(position integer primary key, sequence integer, reference real, offset real, value real)"
        )
        rows = []
        count = 0
        order_errors = []
        previous = None
        with path.open("rb") as f:
            for raw in f:
                digest.update(raw)
                if not raw.strip():
                    continue
                event = json.loads(raw)
                seq = event["sequence"]
                ref = event["reference_ms"]
                offset = event["source_ms"] - ref
                value = event["value"]
                if not isinstance(seq, int) or not all(
                    math.isfinite(v) for v in [ref, offset, value]
                ):
                    raise ValueError("Invalid finite event schema")
                if (
                    previous is not None
                    and seq < previous
                    and len(order_errors) < limit
                ):
                    order_errors.append(count)
                previous = seq
                rows.append((count, seq, ref, offset, value))
                count += 1
                if len(rows) == 2000:
                    db.executemany("insert into events values(?,?,?,?,?)", rows)
                    rows = []
        db.executemany("insert into events values(?,?,?,?,?)", rows)
        db.commit()
        db.execute("create index seq_index on events(sequence)")
        duplicates = db.execute(
            "select sequence,count(*) from events group by sequence having count(*)>1 order by sequence limit ?",
            (limit,),
        ).fetchall()
        duplicate_groups = db.execute(
            "select count(*) from (select sequence from events group by sequence having count(*)>1)"
        ).fetchone()[0]
        missing = []
        missing_count = 0
        previous = None
        for (seq,) in db.execute(
            "select distinct sequence from events order by sequence"
        ):
            if previous is not None and seq > previous + 1:
                missing_count += seq - previous - 1
                if len(missing) < limit:
                    missing.append([previous + 1, seq - 1])
            previous = seq
        # Numerically stable online centered covariance avoids raw timestamp cancellation.
        n = 0
        mx = my = cov = vx = 0.0
        for n, (x, y) in enumerate(
            db.execute("select reference,offset from events"), start=1
        ):
            dx = x - mx
            mx += dx / n
            dy = y - my
            my += dy / n
            cov += dx * (y - my)
            vx += dx * (x - mx)
        drift = cov / vx if vx else None
        after = path.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise RuntimeError("Source changed during analysis; reject results")
        result = {
            "sha256": digest.hexdigest(),
            "records": count,
            "duplicate_groups": duplicate_groups,
            "duplicates": duplicates,
            "missing_count": missing_count,
            "missing_ranges": missing,
            "out_of_order_positions": order_errors,
            "clock_drift_ratio": drift,
            "runtime_s": time.perf_counter() - start,
            "bounded_batch_records": 2000,
            "sqlite_cache_kib": 8192,
            "finding_limit": limit,
            "limitations": "Bounded output may truncate findings; ordering/dedup/drift only. No source modifications.",
        }
        db.close()
        return result
