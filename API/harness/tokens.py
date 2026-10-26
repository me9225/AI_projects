from __future__ import annotations
import json, time
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"

def start_metrics(implementation: str) -> dict:
    return {"implementation": implementation, "started_at": time.perf_counter(),
            "model_calls": 0, "tool_calls": 0, "prompt_tokens": 0,
            "completion_tokens": 0, "total_tokens": 0, "errors": []}

def record_usage(metrics: dict, usage):
    metrics["model_calls"] += 1
    if usage:
        metrics["prompt_tokens"] += getattr(usage, "prompt_tokens", 0) or 0
        metrics["completion_tokens"] += getattr(usage, "completion_tokens", 0) or 0
        metrics["total_tokens"] += getattr(usage, "total_tokens", 0) or 0

def finish_metrics(metrics: dict) -> dict:
    metrics["runtime_seconds"] = round(time.perf_counter() - metrics.pop("started_at"), 4)
    return metrics

def save_metrics(metrics: dict, filename: str = "metrics.jsonl"):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with (RESULTS_DIR / filename).open("a", encoding="utf-8") as f:
        f.write(json.dumps(metrics, ensure_ascii=False) + "\n")
