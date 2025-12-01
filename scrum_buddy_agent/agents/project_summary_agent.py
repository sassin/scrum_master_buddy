from google.adk.agents import Agent
from pathlib import Path
import json
import os

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BASE_DIR / "resource" / "SprintCompass"

REQUIRED_FILES = [
    "project_overview.txt",
    "project_timeline.txt",
    "working_agreements.txt",
    "current_sprint.json",
]


def load_project_files() -> dict:
    """
    TOOL: Loads all required project files for SprintCompass.

    Returns dict:
        - status: success | error
        - files: { file_name: content }
        - error_message: (on error)

    No parameters are needed — the tool always loads the known project files.
    """

    collected = {}

    for filename in REQUIRED_FILES:
        full_path = PROJECT_DIR / filename

        if not full_path.exists():
            return {
                "status": "error",
                "error_message": f"Missing required file: {full_path}",
            }

        try:
            if filename.endswith(".json"):
                with open(full_path, "r", encoding="utf-8") as f:
                    collected[filename] = json.load(f)
            else:
                with open(full_path, "r", encoding="utf-8") as f:
                    collected[filename] = f.read()

        except Exception as e:
            return {
                "status": "error",
                "error_message": f"Failed to load {filename}: {e}",
            }

    return {
        "status": "success",
        "files": collected
    }


ProjectSummaryAgent = Agent(
    name="project_summary_agent",
    model="gemini-2.5-flash",
    description="Loads and summarizes all project documents from SprintCompass.",
    instruction="""
You are the Project Summary Agent for the SprintCompass project.

You ALWAYS start your workflow by calling the `load_project_files` tool.
Do NOT expect parameters — it always loads the required SprintCompass project files:

    - project_overview.txt
    - project_timeline.txt
    - team_work_agreement.txt
    - current_sprint.json

Your job:
1. Load all files using the tool.
2. Summarize the project for the orchestrator agent:
   - Overall project purpose
   - Timeline & milestones
   - Team work norms
   - Current sprint status (stories, risks, ownership)
3. Produce a structured summary: 
   *Project Summary*, *Timeline*, *Team Norms*, *Current Sprint*, *Risks*, *Important Notes*

If any file is missing or unreadable, report exactly which file and why.
""",
    tools=[load_project_files],
    output_key="project_summary"
)