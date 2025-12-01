import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

# Load .env
load_dotenv()

# Read token from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is missing. Add it to your .env file.")

# MCP GitHub Server
mcp_git_server = McpToolset(
    connection_params=StreamableHTTPServerParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-MCP-Toolsets": "all",
            "X-MCP-Readonly": "true"
        },
    ),
)

GitHubAgent = Agent(
    model="gemini-2.5-flash",
    name="github_agent",
    instruction="Help users get information and issue lists from GitHub repository.",
    tools=[mcp_git_server],
)