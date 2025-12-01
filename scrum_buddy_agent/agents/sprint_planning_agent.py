from google.adk.agents import Agent
from pathlib import Path
import json

# This file is: scrum_buddy_agent/agents/sprint_planning_agent.py
# So parent.parent = scrum_buddy_agent/
BASE_DIR = Path(__file__).resolve().parent.parent
BACKLOG_DIR = BASE_DIR / "resource" / "SprintCompass"


def load_backlog_items() -> dict:
    """
    TOOL: Load backlog items from backlog_items.json

    Returns:
        dict with:
        - status: "success" | "error"
        - items: list[dict] (when success)
        - error_message: str (when error)
    """
    backlog_file = BACKLOG_DIR / "backlog_items.json"

    if not backlog_file.is_file():
        return {
            "status": "error",
            "error_message": f"Backlog file not found: {backlog_file}",
        }

    try:
        with backlog_file.open("r", encoding="utf-8") as f:
            items = json.load(f)
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to read backlog file '{backlog_file}': {e}",
        }

    return {
        "status": "success",
        "items": items,
    }


def load_sprint_capacity() -> dict:
    """
    TOOL: Load sprint capacity from sprint_capacity.json

    Returns:
        dict with:
        - status: "success" | "error"
        - capacity: dict (when success)
        - error_message: str (when error)
    """
    capacity_file = BACKLOG_DIR / "sprint_capacity.json"

    if not capacity_file.is_file():
        return {
            "status": "error",
            "error_message": f"Sprint capacity file not found: {capacity_file}",
        }

    try:
        with capacity_file.open("r", encoding="utf-8") as f:
            capacity = json.load(f)
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to read sprint capacity file '{capacity_file}': {e}",
        }

    return {
        "status": "success",
        "capacity": capacity,
    }


SprintPlanningAgent = Agent(
    name="sprint_planning_agent",
    model="gemini-2.5-flash",
    description="Agent that plan the next sprint by selecting backlog items based on goal of the sprint, capacity and priority.",
    instruction="""
You are a Sprint Planning assistant for a Scrum team.

You have access to:
- load_backlog_items(): current product backlog.
- load_sprint_capacity(): team capacity for the upcoming sprint.

When the user asks to plan a sprint:
1. Call both tools to get backlog and capacity.
2. Select a set of backlog items that fits roughly within the total story point capacity.
3. Prefer higher-priority items and ensure a reasonable mix of tech debt, bugs, and features.
4. Group the output into:
   - Sprint goal summary
   - Selected stories (with IDs, titles, story points, and owners if present)
   - Stretch goals (if capacity allows)
   - Risks / dependencies to watch
5. Response is for a base agent.

If data is missing or tools return an error, clearly explain what is missing.
""",
    tools=[load_backlog_items, load_sprint_capacity],
    output_key="sprint_plan"
)