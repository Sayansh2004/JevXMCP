from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from src.config import settings

# Knowledge Base Sample Data
SAMPLE_DOCS = [
    Document(
        page_content="Our subscription return policy allows full refunds within 14 days of initial purchase."
    ),
    Document(
        page_content="To cancel your subscription, navigate to Account Settings -> Billing -> Cancel Subscription."
    ),
    Document(
        page_content="Users can publish up to 50 stories per month on the Pro plan and 5 on the Free plan."
    ),
]


class LightRAG:
    def __init__(self):
        self.vector_store = InMemoryVectorStore(
            embedding=OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=settings.OPENAI_API_KEY,
            )
        )

    async def initialize(self):
        await self.vector_store.aadd_documents(SAMPLE_DOCS)

    async def search(self, query: str, k: int = 2) -> str:
        results = await self.vector_store.asimilarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in results])


rag_system = LightRAG()