from google.adk.agents import Agent
from pathlib import Path
import glob
import os
import vertexai


BASE_DIR = Path(__file__).resolve().parents[1]
RETRO_DIR = BASE_DIR / "resource" / "SprintCompass"


def load_latest_retro_notes() -> dict:
    """
    TOOL: load the latest retrospective notes from disk.

    Looks in RETRO_DIR for *.txt files, picks the most recently modified one,
    and returns its content.

    Returns:
        dict with:
        - status: "success" | "error"
        - file_name: str (when success)
        - notes: str (when success)
        - error_message: str (when error)
    """
    if not RETRO_DIR.is_dir():
        return {
            "status": "error",
            "error_message": f"Retro folder not found: {RETRO_DIR}",
        }

    pattern = str(RETRO_DIR / "*.txt")
    files = glob.glob(pattern)

    if not files:
        return {
            "status": "error",
            "error_message": f"No retro notes found in: {RETRO_DIR}",
        }

    latest_file = RETRO_DIR / "retro_sprint3.txt"

    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to read retro file '{latest_file}': {e}",
        }

    return {
        "status": "success",
        "file_name": os.path.basename(latest_file),
        "notes": content,
    }


RetroAgent = Agent(
    name="retro_agent",
    model="gemini-2.5-flash",
    description="Agent that summarizes sprint retrospectives and proposes action items.",
    instruction="""
You are a Retrospective assistant for a Scrum team.

You have access to:
- load_latest_retro_notes(): raw notes/transcript from the latest sprint retrospective.

When the user asks for a retro summary:
1. Call load_latest_retro_notes().
2. From the notes, extract and organize a summary for sprint retrospection

If the notes are missing or the tool errors, explain what is missing and what the team should provide.
""",
    tools=[load_latest_retro_notes],
    output_key="sprint_retro"
)