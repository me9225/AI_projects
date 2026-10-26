from __future__ import annotations
import json
from shared.tool_schemas import TOOL_SCHEMAS
from shared.dispatch import dispatch_tool
from API.harness.tokens import start_metrics, record_usage, finish_metrics, save_metrics
from API.harness.context import build_messages
from API.harness.memory import load_memory, save_memory

MODEL = __import__("os").getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

def run_agent(client, request: str, session_id: str = "default",
              implementation: str = "API", max_steps: int = 6,
              event_details: dict | None = None, persist_metrics: bool = True) -> str:
    memory = load_memory()
    messages = build_messages(request, memory, event_details)
    messages.append({"role": "user", "content": request})
    metrics = start_metrics(implementation)
    recent_results = []
    try:
        for _ in range(max_steps):
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=TOOL_SCHEMAS,
                tool_choice="auto", temperature=0.2,
            )
            record_usage(metrics, getattr(response, "usage", None))
            choice = response.choices[0]
            msg = choice.message
            assistant_message = {"role": "assistant", "content": msg.content or ""}
            tool_calls = getattr(msg, "tool_calls", None)
            if not tool_calls:
                answer = msg.content or ""
                if persist_metrics:
                    save_metrics(finish_metrics(metrics))
                return answer
            assistant_message["tool_calls"] = [
                {"id": tc.id, "type": "function", "function": {
                    "name": tc.function.name, "arguments": tc.function.arguments
                }} for tc in tool_calls
            ]
            messages.append(assistant_message)
            for tc in tool_calls:
                metrics["tool_calls"] += 1
                try:
                    args = json.loads(tc.function.arguments or "{}")
                    result = dispatch_tool(tc.function.name, args)
                except Exception as exc:
                    metrics["errors"].append(str(exc))
                    result = {"error": str(exc)}
                recent_results.append({"tool": tc.function.name, "result": result})
                messages.append({"role": "tool", "tool_call_id": tc.id,
                                 "content": json.dumps(result, ensure_ascii=False, default=str)})
            # Keep system/context messages and a recent tail after a completed tool cycle.
            if len(messages) > 18:
                messages = messages[:2] + messages[-12:]
        answer = "לא התקבלה תשובה סופית מהמודל לפני מגבלת הצעדים."
        if persist_metrics:
            save_metrics(finish_metrics(metrics))
        return answer
    except Exception as exc:
        metrics["errors"].append(str(exc))
        if persist_metrics:
            save_metrics(finish_metrics(metrics))
        raise
