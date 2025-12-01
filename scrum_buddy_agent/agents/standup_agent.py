from google.adk.agents import Agent
from pathlib import Path
import vertexai
import os
import glob

BASE_DIR = Path(__file__).resolve().parents[1]
TRANSCRIPTS_DIR = BASE_DIR / "resource" / "SprintCompass"

def load_standup_transcript()->dict:
    """
    TOOL: load the stand-up transcript from disk based on users need

    Looks in TRANSCRIPTS_DIR for *.txt files, pick any file

    Returns:
        dict with:
        - status:"success"|"error",
        - file_name:str (when success)
        - transcript: str (when success)
        - error_message: str (when success)
    """

    if not os.path.isdir(TRANSCRIPTS_DIR):
        return {
            "status":"error",
            "error_message":f"Transcript folder not found: {TRANSCRIPTS_DIR}",
        }
    

    latest_file = TRANSCRIPTS_DIR / "standup_current.txt"

    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {
            "status":"error",
            "error_message":f"Transcript folder not found: {TRANSCRIPTS_DIR}",
        }

    return {
        "status": "success",
        "file_name": os.path.basename(latest_file),
        "transcript": content,
    }


StandupSummaryAgent = Agent(
    name="Standup_Summary_Agent",
    model="gemini-2.5-flash-lite",
    instruction="""
You are the stand-up summarizer agent...

    Your job:
    1. Get the stand up transcripts using `load_standup_transcript` tool.
    2. From the file data understand which date's standup updates are being shared
    
    From the transcript, extract **for each person**:
    - Closed / completed issues (with any ticket IDs mentioned).
    - Issues currently being worked on.
    - Blockers (and who needs to help, if clear).
    - Follow-up actions / owners / due dates if mentioned.

    If the tool returns an error, clearly explain what went wrong and suggest how to fix it
    (e.g., create a transcript file, check the folder path, etc.).

    Be concise, but make sure the summary would be directly usable by a PM capturing
    stand-up notes in a tracking system.
""",
    tools=[load_standup_transcript],
    output_key="daily_standup"
)