import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("bridge", Path("tools/workbench_mcp.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
x = m.run_command(
    "node --version && npm --version && npx --version && scripts/local-agent-capability-test.sh"
)
assert x["exit_code"] == 0, x
assert m.run_python("assert 6*7==42; print(42)")["exit_code"] == 0
assert (
    m.run_python(
        "import scipy; import duckdb; assert duckdb.sql('select 385').fetchone()[0]==385",
        runtime="quant",
    )["exit_code"]
    == 0
)
assert (
    m.run_python(
        "import torch; assert torch.arange(10.,device='cuda').square().sum().cpu().item()==285",
        runtime="gpu",
    )["exit_code"]
    == 0
)
assert m.run_command("exit 17")["exit_code"] == 17
assert m.run_command("sleep 5", timeout_seconds=1)["timed_out"]
try:
    m.safe_path("/etc/passwd")
    raise AssertionError("Path escape accepted")
except ValueError:
    pass
print(
    "Bridge PASS: Node PATH, capabilities, Python, failure exit code, timeout, scoped document paths"
)
