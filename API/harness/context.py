import json

SYSTEM_PROMPT = """You are a venue recommendation agent.
Use tools for venue facts; do not invent venue details.
The current user request overrides remembered defaults for this request.
Do not save a preference unless the user explicitly asks you to remember it.
When presenting a venue, include its id and cite source_page if available.
Use get_weather only when weather is relevant or requested.
"""

def build_messages(request: str, memory: dict, event_details: dict | None = None,
                   recent_results: list | None = None) -> list[dict]:
    context = {
        "remembered_preferences": memory,
        "event_details": event_details or {},
        "recent_tool_results": recent_results or [],
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": "Compact context JSON:\n" + json.dumps(context, ensure_ascii=False)}
    ]
