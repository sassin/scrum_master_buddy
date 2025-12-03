import os
import vertexai
import glob
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import AgentTool, FunctionTool
from google.api_core import retry
from google.adk.sessions import InMemorySessionService
from google.adk.apps.app import EventsCompactionConfig
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from pathlib import Path
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.plugins.logging_plugin import (
    LoggingPlugin,
)
import asyncio
from .agents.standup_agent import StandupSummaryAgent
from .agents.sprint_planning_agent import SprintPlanningAgent
from .agents.retro_agent import RetroAgent
from .agents.project_summary_agent import ProjectSummaryAgent
from .agents.agile_coach_agent import AgileCoachAgent
from .agents.github_agent import GitHubAgent
load_dotenv()

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

APP_NAME = "scrum_master_buddy"  # Application
USER_ID = "default"  # User
SESSION = "default"  # Session
MODEL_NAME = "gemini-2.5-flash-lite"
session_service = InMemorySessionService()

events_compaction_config=EventsCompactionConfig(
    compaction_interval=3,
    overlap_size=1,
)


root_agent = Agent(
    name="scrum_master_buddy",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="An enterprise Scrum Master buddy that helps PMs with all the scrum master related roles.",
    instruction="""

You are seasoned Scrum Master helping product owners to run their agile and sprint process smoothly. 
Reply to users query in a way that is easy to comprehend and do not over burden with information unless especificaly reqeusted. 
You are a pragmatic assistant and provide the information only if requested.

You have access to following sub agents:
1. SprintPlanningAgent:
   - This agent can help to plan a sprint using items in backlog and capacity of the team for next sprint.

2. StandupSummaryAgent:
   - This agent provides a summaray of last standup, it provides status by person, blockers, or follow-ups.

3. RetroAgent:
   - Use this agent when you want to understand what happen in the last sprint and understand the learnings of the last sprint

4. ProjectSummaryAgent
    - Reach out to this agent for project summary, current sprint and issues, and related questions.

5. AgileCoachAgent
    - This agent is your mentor in following the best agile and scrum practices. 
    - This agent can help you to learn best practices to follow based on your project situation.  

6. GitHubAgent
    - This agent can load issue from github when required

Behavior:
    - Do not assume anything, always ask clarifying questions.
    - Use agents as necessary for the context of the query.
    - Think quitely after gathering the required information and understanding the context.

when working with observability, only show the final required information to user.
Be concise but helpful. Always think like a pragmatic Scrum Master working with a busy PM.
""",
#    tools=[AgentTool(StandupSummaryAgent),AgentTool(SprintPlanningAgent),AgentTool(RetroAgent)],
tools=[ AgentTool(ProjectSummaryAgent), 
        AgentTool(StandupSummaryAgent), 
        AgentTool(RetroAgent), 
        AgentTool(SprintPlanningAgent), 
        AgentTool(AgileCoachAgent), 
        AgentTool(GitHubAgent)
        ],
)

scrum_buddy = App(
    name="project_coordinator",
    root_agent=root_agent,
    plugins=[LoggingPlugin()],
    events_compaction_config=events_compaction_config,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

Runner(
    app=scrum_buddy,
    session_service=session_service,
)



