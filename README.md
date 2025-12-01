Scrum Masters and PMs juggle countless responsibilities—managing standups, retrospectives, sprint planning, backlog refinement, tracking risks, coordinating with UX/DevOps/QA, and ensuring the Agile process actually delivers value.
This becomes overwhelming in fast-moving teams.

Agents allow the system to work like a real Scrum Master:
Specialized sub-agents handle specific workflows
Root agent decides which sub-agent to call
Tools load live sprint data, project docs, backlog JSON
Google Search provides best-practice coaching
GitHub MCP agent fetches real issues
Modular, extensible, and maintainable
Traditional chatbots cannot orchestrate this level of workflow specialization.

Root Agent
The orchestrator. Decides which subagent to call based on user query.

Sub Agents
StandupSummaryAgent: Extracts yesterday/today/blockers from transcripts
SprintPlanningAgent: Uses backlog + capacity JSONs to plan next sprint
RetroAgent: Summarizes retrospective notes into action items
ProjectSummaryAgent: Loads project overview, timeline, agreements, and sprint JSON
AgileCoachAgent: Uses Google Search for agile best practices
GitHubAgent: Uses MCP GitHub server to pull issues

Tools
Custom JSON loaders
TXT file loaders
Google Search
GitHub MCP Toolset

DEMO Flow:
User: “Summarize the latest standup.”
Root Agent → StandupSummaryAgent → load_standup_transcript() → returns structured summary
User: “Plan the next sprint.”
Root Agent → SprintPlanningAgent → load_backlog_items() + load_sprint_capacity() → returns plan
User: “Why are items rolling over? What should we do?”
Root Agent → AgileCoachAgent → Google Search → context-aware agile advice

Multi Agent Overview:

                +------------------------+
                |  Scrum Master Buddy    |
                |      (Root Agent)      |
                +-----------+------------+
                            |
  -----------------------------------------------------------------------
  |               |                 |             |             |        |
  v               v                 v             v             v        v
StandupAgent   SprintPlan     RetroAgent   ProjectSummary   AgileCoach   GitHubAgent
Reads TXT      Reads JSON     Reads retro  Reads all docs   Google       MCP GitHub



Data Structure of a sample project names SprintCompass:
SprintCompass/
│
├── project_overview.txt
├── project_timeline.txt
├── working_agreements.txt
├── current_sprint.json
├── backlog_items.json
├── sprint_capacity.json
└── standup_current.txt


Sample Data:
The json files and txt files all are just representative of project artifacts, in the production version this should be linked to JIRA, confluence or other project management tools where the agent can find the sprint, backlog, call transcript and project artifacts.
