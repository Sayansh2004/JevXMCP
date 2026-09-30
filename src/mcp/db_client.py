
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Define how to launch the MCP server subprocess
server_params = StdioServerParameters(
    command=sys.executable,  # Uses the active python interpreter
    args=["src/mcp/db_server.py"],
    env=None
)

async def call_mcp_db_tool(query: str, auth_code: str = "") -> str:
    """Connects to the MCP Database Server over stdio and executes the query."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection handshake with MCP server
            await session.initialize()
            
            # Execute the remote tool via MCP standard
            result = await session.call_tool(
                "execute_sql_query", 
                arguments={"query": query, "auth_code": auth_code}
            )
            
            # Return text response from MCP tool content block
            return result.content[0].text