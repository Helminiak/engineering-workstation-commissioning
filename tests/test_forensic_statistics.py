import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from commissioning_statistics import pearson, performance_regression

x = list(range(100))
y = [2 * v + 7 for v in x]
r = pearson(x, y)
assert abs(r - 1) < 1e-12
slow = performance_regression([1, 1.01, 0.99], [2, 2.01, 1.99])
assert slow["regression"] and slow["relative_change"] == 1
stable = performance_regression([1, 1.01, 0.99], [1.01, 1.02, 1])
assert not stable["regression"]
try:
    pearson([1, 1, 1], [2, 3, 4])
    raise AssertionError("Undefined correlation accepted")
except ValueError:
    pass
(ROOT / "evidence/forensic-statistics.json").write_text(
    json.dumps(
        {
            "status": "PASS",
            "correlation": r,
            "planted_regression": slow,
            "stable_case": stable,
        },
        indent=2,
    )
    + "\n"
)
print("PASS correlation and planted/stable benchmark regression detection")
