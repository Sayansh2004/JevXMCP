from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

llm=ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
)

from mcp.db_server import sql_read_query, sql_write_mutation

tools=[sql_read_query, sql_write_mutation]

llm_with_tools=llm.bind_tools(tools)