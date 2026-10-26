from shared.venue_tools import search_venues, get_venue_details
from shared.external_tools import get_weather

TOOL_FUNCTIONS = {
    "search_venues": search_venues,
    "get_venue_details": get_venue_details,
    "get_weather": get_weather,
}

def dispatch_tool(name: str, arguments: dict):
    if name not in TOOL_FUNCTIONS:
        raise ValueError(f"Unknown tool: {name}")
    return TOOL_FUNCTIONS[name](**arguments)
