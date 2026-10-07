import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from commissioning_rag import Index

folder = ROOT / "datasets/rag-fixture"
folder.mkdir(exist_ok=True)
docs = {
    "handoff.md": "The workstation recovery target is five minutes. A new agent reads NEXT_AGENT.md and progress.json after an interruption.",
    "security.md": "Credentials and passwords must never be committed. Agent servers bind to localhost and require authentication.",
    "gpu.json": json.dumps(
        {"gpu": "NVIDIA RTX 5090", "context_tokens": 32768, "free_memory_gib": 6.7}
    ),
    "forensics.csv": "item,rule\noriginal evidence,never modify\nprovenance,SHA-256 hashing\n",
}
for name, text in docs.items():
    (folder / name).write_text(text)
idx = Index(ROOT / "rag/synthetic-index.sqlite", folder)
start = time.perf_counter()
changed = idx.update()
assert not idx.stale()
assert not idx.update()
exact = idx.retrieve('"five minutes"', False)
assert exact[0]["path"].endswith("handoff.md")
questions = [
    ("What is the recovery time objective after a crash?", "handoff.md"),
    ("How should secret passwords be handled in version control?", "security.md"),
    ("What graphics card and context size does this machine use?", "gpu.json"),
]
results = []
for q, want in questions:
    hits = idx.retrieve(q)
    assert hits[0]["path"].endswith(want), (q, hits)
    results.append({"question": q, "expected": want, "hits": hits})
p = folder / "handoff.md"
p.write_text(p.read_text() + "\nIncremental update marker.")
assert idx.stale()
try:
    idx.retrieve("crash")
    raise AssertionError("Stale retrieval accepted")
except ValueError:
    pass
assert idx.update()
assert not idx.stale()
r = {
    "status": "PASS",
    "semantic_top1_accuracy": 1.0,
    "known_answer_queries": len(questions),
    "incremental_indexing": True,
    "stale_detection": True,
    "exact_retrieval": True,
    "source_citations": True,
    "runtime_s": time.perf_counter() - start,
    "results": results,
    "limitations": "Local synthetic fixtures only; PDF extraction supported but OCR is not; no personal directories indexed.",
}
(ROOT / "evidence/rag-validation.json").write_text(json.dumps(r, indent=2) + "\n")
print(
    "PASS: local embedding retrieval, exact lookup, 3/3 known answers, incremental update and stale detection"
)
