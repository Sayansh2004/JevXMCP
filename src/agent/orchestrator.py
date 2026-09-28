import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from src.agent.llm import synthesis_llm
from src.mcp.db import db

console = Console()


async def generate_sql_query(user_prompt: str) -> str:
    """Uses System 2 LLM to generate raw PostgreSQL query."""
    system_message = (
        "You are a PostgreSQL expert. Convert the user request into valid SQL "
        "for the 'users' table (columns: id, name, email, age, stories_count, about). "
        "Return ONLY the SQL string without markdown formatting or backticks."
    )
    prompt = f"{system_message}\n\nUser Request: {user_prompt}"
    response = await synthesis_llm.ainvoke(prompt)
    return response.content.strip()


async def execute_db_pipeline(user_prompt: str):
    """Phase 1 Pipeline: SQL Generation -> Security Intercept -> MCP Tool Execution -> Synthesis"""
    console.print(f"\n[bold cyan]User Request:[/] {user_prompt}")

    # 1. Generate SQL query
    sql_query = await generate_sql_query(user_prompt)
    console.print(f"[bold yellow]Generated SQL:[/] {sql_query}")

    # 2. Inspect query type & Step-Up Authorization (HITL)
    is_delete = "DELETE" in sql_query.upper()
    confirmation_code = ""

    if is_delete:
        console.print(
            Panel(
                f"[bold red]SECURITY INTERCEPT:[/] Destructive query detected:\n[cyan]{sql_query}[/]",
                title="Step-Up Authorization Required",
            )
        )
        # Interactive CLI prompt for authorization secret code
        confirmation_code = Prompt.ask(
            "[bold yellow]Enter Authorization Secret Code to proceed[/]"
        )

    # 3. Execute query via asyncpg DB interface
    if is_delete or "INSERT" in sql_query.upper() or "UPDATE" in sql_query.upper():
        db_result = await db.execute_write_mutation(
            sql_query, confirmation_code=confirmation_code
        )
    else:
        db_result = await db.execute_read_query(sql_query)

    console.print(f"[bold green]Database Execution Result:[/] {db_result}")

    # 4. Handle rejection or synthesize final response
    if db_result.get("status") == "rejected":
        console.print(
            f"[bold red]❌ Execution Aborted:[/] {db_result.get('message')}"
        )
        return db_result.get("message")

    # Synthesize answer
    synthesis_prompt = (
        f"User asked: {user_prompt}\n"
        f"Database returned: {db_result}\n"
        f"Summarize this result clearly for the user."
    )
    final_answer = await synthesis_llm.ainvoke(synthesis_prompt)
    console.print(f"\n[bold magenta]Final Agent Response:[/]\n{final_answer.content}")
    return final_answer.content


if __name__ == "__main__":
    # Quick test runner for Phase 1
    async def test():
        # Test 1: Read Query
        await execute_db_pipeline("Show me all users with more than 10 stories.")

        # Test 2: Destructive Delete Query (Triggers HITL Step-Up Prompt)
        await execute_db_pipeline("Delete user with email alex.rivers@example.com")

        await db.close()

    asyncio.run(test())