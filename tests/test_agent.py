import json
from pathlib import Path
from API.harness.memory import load_memory, save_memory
from shared.venue_tools import search_venues, get_venue_details
from shared.tool_schemas import TOOL_SCHEMAS
from shared.dispatch import dispatch_tool

def test_memory_persists(tmp_path):
    p = tmp_path / "memory.json"
    save_memory({"default_city": "Tel Aviv"}, p)
    save_memory({"preferred_features": ["parking"]}, p)
    data = load_memory(p)
    assert data["default_city"] == "Tel Aviv"
    assert data["preferred_features"] == ["parking"]

def test_search_filters():
    results = search_venues(city="Tel Aviv", min_capacity=60, required_features=["parking"])
    assert all(v["city"] == "Tel Aviv" and v["capacity"] >= 60 and "parking" in v["features"] for v in results)

def test_details_found():
    assert get_venue_details("demo-001")["name"] == "Demo Hall A"

def test_shared_tools_include_external():
    names = {x["function"]["name"] for x in TOOL_SCHEMAS}
    assert {"search_venues", "get_venue_details", "get_weather"} <= names
    assert dispatch_tool("get_venue_details", {"venue_id": "demo-002"})["city"] == "Jerusalem"

def test_unknown_tool():
    try:
        dispatch_tool("does_not_exist", {})
    except ValueError as e:
        assert "Unknown tool" in str(e)
    else:
        assert False, "Expected ValueError"
