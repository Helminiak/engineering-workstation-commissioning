import json
import statistics
import subprocess
import threading
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = Path("/home/joe/.lmstudio/credentials/local-work-api.token").read_text().strip()


def request(data):
    req = urllib.request.Request(
        "http://127.0.0.1:1234/v1/chat/completions",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + KEY},
    )
    return urllib.request.urlopen(req, timeout=240)


def gpu():
    row = (
        subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu",
                "--format=csv,noheader,nounits",
            ],
            text=True,
        )
        .strip()
        .split(", ")
    )
    return dict(
        zip(
            ["memory_mib", "total_mib", "utilization_percent", "temperature_c"],
            map(int, row),
        )
    )


context = int(__import__("sys").argv[1])
rows = []
for repeat in range(3):
    samples = []
    stop = threading.Event()

    def sample(stop=stop, samples=samples):
        while not stop.is_set():
            samples.append(gpu())
            stop.wait(0.5)

    thread = threading.Thread(target=sample)
    thread.start()
    start = time.monotonic()
    first = None
    events = []
    text = ""
    usage = {}
    payload = {
        "model": "qwen/qwen3.8-27b",
        "messages": [
            {
                "role": "user",
                "content": ("The calibrated value is 385.\n" * 300)
                + f"Benchmark trial {repeat}: Explain the sum of squares formula briefly, then list squares of integers 1 through 20. /no_think",
            }
        ],
        "stream": True,
        "stream_options": {"include_usage": True},
        "max_tokens": 1500,
        "temperature": 0,
        "reasoning_effort": "none",
    }
    try:
        with request(payload) as stream:
            for line in stream:
                line = line.decode().strip()
                if not line.startswith("data: ") or line == "data: [DONE]":
                    continue
                event = json.loads(line[6:])
                events.append(event)
                if event.get("usage"):
                    usage = event["usage"]
                for choice in event.get("choices", []):
                    content = choice.get("delta", {}).get("content") or ""
                    if content and first is None:
                        first = time.monotonic()
                    text += content
    finally:
        stop.set()
        thread.join()
    end = time.monotonic()
    (ROOT / f"evidence/llm-stream-{context}-{repeat}.json").write_text(
        json.dumps(events, indent=2)
    )
    if first is None:
        raise AssertionError("No visible text; see captured stream")
    row = {
        "repeat": repeat,
        "context": context,
        "time_to_first_token_s": first - start,
        "elapsed_s": end - start,
        "completion_tokens": usage.get("completion_tokens"),
        "prompt_tokens": usage.get("prompt_tokens"),
        "peak_vram_mib": max(x["memory_mib"] for x in samples),
        "peak_gpu_utilization_percent": max(x["utilization_percent"] for x in samples),
        "gpu_samples": samples,
        "answer": text,
    }
    row["generation_tokens_per_second"] = usage.get("completion_tokens", 0) / max(
        end - first, 0.001
    )
    rows.append(row)
# Exact JSON correctness separately.
payload = {
    "model": "qwen/qwen3.8-27b",
    "messages": [
        {
            "role": "user",
            "content": "Return sum of squares of 1..10 as total. /no_think",
        }
    ],
    "temperature": 0,
    "max_tokens": 1500,
    "reasoning_effort": "none",
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "result",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {"total": {"type": "integer"}},
                "required": ["total"],
                "additionalProperties": False,
            },
        },
    },
}
with request(payload) as f:
    x = json.load(f)
assert json.loads(x["choices"][0]["message"]["content"]) == {"total": 385}
summary = {
    "context": context,
    "repeats": 3,
    "median_ttft_s": statistics.median(x["time_to_first_token_s"] for x in rows),
    "median_generation_tokens_per_second": statistics.median(
        x["generation_tokens_per_second"] for x in rows
    ),
    "peak_vram_mib": max(x["peak_vram_mib"] for x in rows),
    "structured_output_verified": True,
    "rows": rows,
    "limitations": "Short ~3K input benchmark; capacity allocation and inference verified, near-limit long-context accuracy and prompt throughput not measured.",
}
(ROOT / f"evidence/llm-benchmark-{context}.json").write_text(
    json.dumps(summary, indent=2) + "\n"
)
print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, indent=2))
