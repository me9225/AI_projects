"""Runs a simple two-session scenario. It persists explicit memory updates between turns."""
import json
from pathlib import Path
from dotenv import load_dotenv
from API.agent import run_agent
from API.harness.memory import save_memory, load_memory

ROOT = Path(__file__).resolve().parent

def main():
    load_dotenv()
    scenario = json.loads((ROOT / "scenario.json").read_text(encoding="utf-8"))
    out = []
    for session in scenario["sessions"]:
        session_result = {"session_id": session["session_id"], "turns": []}
        for turn in session["turns"]:
            if turn.get("memory_update"):
                save_memory(turn["memory_update"])
            answer = run_agent(turn["user"], session_id=session["session_id"])
            session_result["turns"].append({
                "user": turn["user"], "answer": answer, "memory_after": load_memory()
            })
        out.append(session_result)
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "scenario_results.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote results/scenario_results.json")

if __name__ == "__main__":
    main()
