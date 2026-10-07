import json
import statistics
import sys
import time
import tracemalloc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from commissioning_mbo import Book


def workload(rounds=5, depth=200):
    book = Book()
    events = 0

    def apply(e):
        nonlocal events
        e["sequence"] = book.sequence + 1
        book.apply(e)
        events += 1

    start = time.perf_counter()
    for r in range(rounds):
        for i in range(depth):
            apply(
                {
                    "type": "add",
                    "id": str(i),
                    "side": "bid" if i % 2 == 0 else "ask",
                    "price": 100 - i % 20 if i % 2 == 0 else 105 + i % 20,
                    "quantity": 10,
                }
            )
        for i in range(depth):
            apply(
                {
                    "type": "modify",
                    "id": str(i),
                    "price": book.orders[str(i)].price,
                    "quantity": 11,
                }
            )
        for i in range(depth):
            apply({"type": "fill", "id": str(i), "quantity": 5})
        for i in range(depth):
            apply({"type": "fill", "id": str(i), "quantity": 6})
        assert not book.orders
    assert book.traded_volume == rounds * depth * 11 and book.delta == 0
    return {"seconds": time.perf_counter() - start, "events": events, "depth": depth}


workload(1, 20)  # Explicit unreported warmup.
rows = [workload() for _ in range(3)]
tracemalloc.start()
memory_trial = workload(1, 200)
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
median = statistics.median(r["seconds"] for r in rows)
report = {
    "status": "PASS",
    "mixed_events": ["add", "modify", "partial fill", "full fill"],
    "repeats": 3,
    "rows": rows,
    "median_seconds": median,
    "median_events_per_second": rows[0]["events"] / median,
    "peak_python_bytes_in_separate_memory_trial": peak,
    "memory_trial": memory_trial,
    "limitations": "Reference implementation copies the book transactionally; synthetic 200-order depth. Memory instrumentation excluded from throughput trials.",
}
(ROOT / "evidence/mbo-mixed-benchmark.json").write_text(
    json.dumps(report, indent=2) + "\n"
)
print(json.dumps(report, indent=2))
