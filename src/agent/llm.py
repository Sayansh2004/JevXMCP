from langchain_openai import ChatOpenAI
from src.config import settings

# System 2 LLM for SQL generation and final answer synthesis
synthesis_llm = ChatOpenAI(
    model=settings.SYNTHESIS_MODEL,
    api_key=settings.OPENAI_API_KEY,
    temperature=0.0,
)