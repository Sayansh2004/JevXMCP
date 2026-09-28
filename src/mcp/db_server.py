import asyncio
from fastmcp import FastMCP
from src.mcp.db import db

# Initialize FastMCP Server for Neon Postgres
mcp = FastMCP("NeonDB Server")


@mcp.tool()
async def sql_read_query(sql_query: str) -> dict:
    """MCP Tool: Execute async SELECT SQL query on the Neon Postgres database."""
    return await db.execute_read_query(sql_query)


@mcp.tool()
async def sql_write_mutation(sql_query: str, confirmation_code: str = "") -> dict:
    """MCP Tool: Execute async INSERT, UPDATE, or DELETE SQL query on Neon Postgres."""
    return await db.execute_write_mutation(sql_query, confirmation_code)


if __name__ == "__main__":
    # Test connection directly using asyncio
    async def main():
        print("Testing Neon Database Connection via asyncpg...")
        res = await db.execute_read_query("SELECT version();")
        print("Database Response:", res)
        await db.close()

    asyncio.run(main())