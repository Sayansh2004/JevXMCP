
from mcp.server.fastmcp import FastMCP
import asyncpg
import os

# Initialize FastMCP Server
mcp = FastMCP("Database-MCP-Server")

@mcp.tool()
async def execute_sql_query(query: str, auth_code: str = None) -> str:
    """Executes SQL queries safely against the PostgreSQL database."""
    
    # HITL Step-Up Auth Check for Destructive Mutations
    normalized = query.strip().upper()
    if any(keyword in normalized for keyword in ["DELETE", "DROP", "TRUNCATE"]):
        if auth_code != "ALLOWED_11111":
            return "ERROR: Step-up authorization failed or missing required auth_code."

    # Connect and Execute
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    try:
        if normalized.startswith("SELECT"):
            records = await conn.fetch(query)
            return str([dict(r) for r in records])
        else:
            status = await conn.execute(query)
            return f"Success: {status}"
    except Exception as e:
        return f"Database Error: {str(e)}"
    finally:
        await conn.close()

if __name__ == "__main__":
    # Runs the server over standard I/O (stdio)
    mcp.run()