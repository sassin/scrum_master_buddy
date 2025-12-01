from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

AgileCoachAgent = Agent(
    name="Agile_Coach_Agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are the **Agile Coach**. 
        -You are called by a higher-level Scrum Master agent whenever guidance is needed: standup smells
        , spillover, quality issues, planning problems, stakeholder pressure, etc.
        
        Your responsibilities:
        1. Read the situation described by the calling agent
        — it may include:
        - project context
        - current sprint health
        - standup summaries
        - retrospection points
        - capacity and upcoming backlog

        2. use google_search tool with a short, focused query such as:
        - "stories rolling over every sprint scrum best practice"
        - "how to handle frequent unplanned work agile"
        - "improve standup effectiveness anti patterns"

        3. Combine three things in your answer:
        - a) Your built-in knowledge of Scrum and agile principles,
        - b) Key ideas from the tool results (titles/snippets),
        - c) The specific project context in the question.

        4. Do **not** just paste raw search results. Interpret them and adapt the advice
        to the project. Be practical and concise.

        Your tone:
        - Supportive, clear, and pragmatic.
        """,
    tools=[google_search],
    output_key="coach_suggestion",  # The result of this agent will be stored in the session state with this key.
)