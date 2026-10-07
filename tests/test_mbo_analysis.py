import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from commissioning_mbo import Book, book_metrics, persistence_events, replay_jsonl

b = Book()
frames = []
b.apply(
    {
        "sequence": 1,
        "type": "add",
        "id": "bid",
        "side": "bid",
        "price": 100,
        "quantity": 10,
    }
)
frames.append(b.snapshot())
b.apply(
    {
        "sequence": 2,
        "type": "add",
        "id": "ask",
        "side": "ask",
        "price": 105,
        "quantity": 5,
    }
)
frames.append(b.snapshot())
m = book_metrics(b)
assert (
    m["bid_volume"] == 10
    and m["ask_volume"] == 5
    and abs(m["imbalance"] - 1 / 3) < 1e-12
    and m["descriptive_regime"] == "bid_heavy"
)
b.apply({"sequence": 3, "type": "fill", "id": "ask", "quantity": 2})
frames.append(b.snapshot())
assert book_metrics(b)["executed_delta"] == 2
b.apply({"sequence": 4, "type": "cancel", "id": "bid"})
frames.append(b.snapshot())
episodes = persistence_events(frames)
assert next(e for e in episodes if e["id"] == "bid")["duration_events"] == 3
assert next(e for e in episodes if e["id"] == "ask")["right_censored"]
first = replay_jsonl(ROOT / "datasets/synthetic-mbo.jsonl").snapshot()
second = replay_jsonl(ROOT / "datasets/synthetic-mbo.jsonl").snapshot()
assert first == second
(ROOT / "evidence/mbo-analysis.json").write_text(
    json.dumps(
        {
            "status": "PASS",
            "metrics": m,
            "persistence": episodes,
            "streaming_replay_deterministic": True,
            "limitations": "Regimes are descriptive volume buckets; persistence uses event sequence, not wall-clock duration. No strategy.",
        },
        indent=2,
    )
    + "\n"
)
print(
    "PASS book volumes/delta, descriptive regimes, persistence intervals and streaming replay"
)
