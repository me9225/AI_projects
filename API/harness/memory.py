from __future__ import annotations
import json, os, tempfile
from pathlib import Path
from threading import RLock

MEMORY_PATH = Path(__file__).resolve().parents[2] / "shared" / "data" / "memory.json"
_LOCK = RLock()

def load_memory(path: Path = MEMORY_PATH) -> dict:
    with _LOCK:
        if not path.exists():
            return {"default_city": None, "preferred_features": [], "last_selected_venue_id": None}
        return json.loads(path.read_text(encoding="utf-8"))

def save_memory(updates: dict, path: Path = MEMORY_PATH) -> dict:
    """Merge updates atomically; only explicitly supplied keys are changed."""
    with _LOCK:
        current = load_memory(path)
        current.update(updates)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix="memory-", suffix=".json", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(current, f, ensure_ascii=False, indent=2)
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        return current

def relevant_memory(request: str, memory: dict) -> dict:
    """Small context: always include defaults and preferences, not the whole conversation."""
    return {
        "default_city": memory.get("default_city"),
        "preferred_features": memory.get("preferred_features", []),
        "last_selected_venue_id": memory.get("last_selected_venue_id"),
    }
