import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from commissioning_mbo import replay_jsonl

source = ROOT / "datasets/synthetic-mbo.jsonl"
tsv = ROOT / "datasets/synthetic-mbo.tsv"
# Numeric absent fields are zero; do not alter the original JSONL.
with tsv.open("w") as out:
    for line in source.read_text().splitlines():
        e = json.loads(line)
        cols = [
            e["sequence"],
            e["type"],
            e.get("id", ""),
            e.get("side", ""),
            e.get("price", 0),
            e.get("quantity", 0),
            e.get("aggressor", ""),
        ]
        out.write("\t".join(map(str, cols)) + "\n")
p = subprocess.run(
    ["java", "-cp", "artifacts/java-mbo/classes", "commissioning.Replay", str(tsv)],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=True,
)
b = replay_jsonl(source)
expected = [f"sequence={b.sequence}", f"volume={b.traded_volume}", f"delta={b.delta}"]
expected += [
    f"order={oid},{o.side},{o.price},{o.quantity},{o.priority}"
    for oid, o in sorted(b.orders.items())
]
assert p.stdout.splitlines() == expected, (p.stdout, expected)
(ROOT / "evidence/cross-language-replay.json").write_text(
    json.dumps(
        {
            "status": "PASS",
            "expected": expected,
            "java_actual": p.stdout.splitlines(),
            "exit_code": p.returncode,
        },
        indent=2,
    )
    + "\n"
)
print("PASS Java/Python deterministic event replay agreement")
