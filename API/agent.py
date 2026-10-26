import os
from groq import Groq
from API.harness.loop import run_agent as run_loop

def run_agent(request: str, session_id: str = "default", event_details: dict | None = None):
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return run_loop(client, request, session_id=session_id, implementation="API",
                    event_details=event_details)
