import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from src.agent.dispatcher import main_dispatcher
from src.mcp.db import db
from src.mcp.rag import rag_system

console = Console()


async def start_interactive_chat():
    # Initialize RAG vector store and DB connections
    await rag_system.initialize()
    
    console.print(
        Panel.fit(
            "[bold green]Jev Agentic System Initialized[/]\n"
            "[dim]Type your message below. Type 'exit' or 'quit' to stop.[/]",
            title="Interactive CLI",
            border_style="cyan"
        )
    )

    try:
        while True:
            user_input = Prompt.ask("\n[bold cyan]You[/]")
            
            if user_input.strip().lower() in ["exit", "quit"]:
                console.print("[yellow]Exiting chat session. Goodbye![/]")
                break
                
            if not user_input.strip():
                continue

            # Pass prompt to the router & dispatcher pipeline
            await main_dispatcher(user_input)

    finally:
        # Graceful cleanup on exit
        await db.close()


if __name__ == "__main__":
    asyncio.run(start_interactive_chat())