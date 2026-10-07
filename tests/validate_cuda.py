import json
import time
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent.parent
assert torch.cuda.is_available()
start = time.perf_counter()
torch.manual_seed(42)
cpu = torch.arange(1024 * 1024, dtype=torch.float32).reshape(1024, 1024) / 1024
x = cpu.to("cuda")
torch.cuda.synchronize()
y = x.square() + 2 * x + 1
torch.cuda.synchronize()
actual = y.cpu()
expected = cpu.square() + 2 * cpu + 1
error = float((actual - expected).abs().max())
assert error <= 0.125, error
small = torch.arange(10.0, device="cuda")
assert small.square().sum().cpu().item() == 285
allocation = torch.empty(64 * 1024 * 1024, dtype=torch.uint8, device="cuda")
allocation.fill_(7)
torch.cuda.synchronize()
assert allocation[0].cpu().item() == 7
result = {
    "status": "PASS",
    "torch": torch.__version__,
    "cuda_runtime": torch.version.cuda,
    "gpu": torch.cuda.get_device_name(0),
    "capability": list(torch.cuda.get_device_capability()),
    "compiled_architectures": torch.cuda.get_arch_list(),
    "runtime_s": time.perf_counter() - start,
    "peak_allocation_bytes": torch.cuda.max_memory_allocated(),
    "transfer_verified": True,
    "max_absolute_error": error,
    "tolerance": 0.125,
    "small_exact_sum": 285,
}
(ROOT / "evidence/cuda-validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
