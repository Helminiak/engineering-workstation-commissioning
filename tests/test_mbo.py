import hashlib
import json
import sys
import time
import tracemalloc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from commissioning_mbo import Book

b = Book()
events = []


def apply(**e):
    e["sequence"] = b.sequence + 1
    b.apply(e)
    events.append(e)


apply(type="add", id="b1", side="bid", price=100, quantity=10)
apply(type="add", id="b2", side="bid", price=100, quantity=5)
apply(type="add", id="a1", side="ask", price=102, quantity=8)
assert b.levels()["bid"][100] == 15
apply(type="modify", id="b1", price=100, quantity=12)
assert b.queue("bid", 100) == ["b2", "b1"]
apply(type="fill", id="a1", quantity=3)
assert b.orders["a1"].quantity == 5
apply(type="fill", id="a1", quantity=5)
assert 102 not in b.levels()["ask"]
assert b.delta == 8
apply(type="cancel", id="b2")
apply(type="cancel", id="b1")
assert not b.orders
apply(type="trade", quantity=2, aggressor="sell")
assert b.delta == 6
for seq in [b.sequence, b.sequence + 2]:
    before = b.snapshot()
    try:
        b.apply({"sequence": seq, "type": "trade", "quantity": 1, "aggressor": "buy"})
        raise AssertionError("Bad sequence accepted")
    except ValueError:
        assert before == b.snapshot()
apply(type="add", id="b", side="bid", price=100, quantity=1)
try:
    b.apply(
        {
            "sequence": b.sequence + 1,
            "type": "add",
            "id": "cross",
            "side": "ask",
            "price": 99,
            "quantity": 1,
        }
    )
    raise AssertionError("Crossed book accepted")
except ValueError:
    assert "cross" not in b.orders
replay = Book()
for e in events:
    replay.apply(e)
assert replay.snapshot() == b.snapshot()
p = ROOT / "datasets/synthetic-mbo.jsonl"
p.write_text("".join(json.dumps(e) + "\n" for e in events))
bench = Book()
tracemalloc.start()
start = time.perf_counter()
for i in range(20000):
    bench.apply({"sequence": i + 1, "type": "trade", "quantity": 1, "aggressor": "buy"})
elapsed = time.perf_counter() - start
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
r = {
    "status": "PASS",
    "cases": [
        "new order",
        "modify/queue reprioritization",
        "partial fill",
        "full fill",
        "cancel",
        "missing message",
        "out-of-order message",
        "crossed-book rejection",
        "price-level deletion",
        "replay determinism",
        "trade/delta",
    ],
    "events": 20000,
    "seconds": elapsed,
    "events_per_second": 20000 / elapsed,
    "peak_python_bytes": peak,
    "fixture_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
    "limitations": "Python reference book only; trade-only throughput is not full order-book throughput. Java pending approved JDK installation. No proprietary data.",
}
(ROOT / "evidence/mbo-validation.json").write_text(json.dumps(r, indent=2) + "\n")
print(json.dumps(r, indent=2))
