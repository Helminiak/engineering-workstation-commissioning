import datetime
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
x = json.loads((ROOT / "scratch/local-agent-science-proof.json").read_text())
linear = x["numpy_scipy_linear_algebra"]
assert np.allclose(linear["solution"], [2, 3], rtol=0, atol=1e-12)
assert linear["exit_code"] == 0
assert (
    x["duckdb_sum_squares"]["result"] == 385
    and x["duckdb_sum_squares"]["exit_code"] == 0
)
assert (
    x["torch_cuda_sum_squares"]["result"] == 285
    and x["torch_cuda_sum_squares"]["exit_code"] == 0
)
p = ROOT / "state/local-agent-science-proof.json"
state = json.loads(p.read_text())
codes = []
for m in state["messages"]:
    if m.get("role") != "tool":
        continue
    result = json.loads(m["content"])
    for content in result["content"]:
        if content.get("type") == "text":
            payload = json.loads(content["text"])
            codes.append(payload["exit_code"])
assert codes.count(0) == 4 and codes.count(1) == 1, codes
state["status"] = "PASS"
state["independent_verification"] = {
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "exit_codes": codes,
    "known_answers": [2, 3, 385, 285],
}
p.write_text(json.dumps(state, indent=2) + "\n")
p.chmod(0o600)
(ROOT / "evidence/local-agent-science-verification.json").write_text(
    json.dumps(state["independent_verification"], indent=2) + "\n"
)
print(
    "PASS: independent model artifact and actual MCP exit-code verification; one diagnosed/repaired failure"
)
