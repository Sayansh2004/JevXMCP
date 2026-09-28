import asyncpg
from typing import Optional
from src.config import settings


class AsyncNeonDB:


    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def get_pool(self) -> asyncpg.Pool:
        """Lazily initializes and returns the asyncpg connection pool."""
        if self.pool is None:
            # asyncpg accepts the standard Neon connection string with sslmode=require
            self.pool = await asyncpg.create_pool(
                dsn=settings.NEON_DATABASE_URL,
                min_size=1,
                max_size=10,
            )
        return self.pool

    async def execute_read_query(self, sql_query: str) -> dict:
        """Executes async SELECT queries and returns results as list of dicts."""
        try:
            pool = await self.get_pool()
            async with pool.acquire() as conn:
                records = await conn.fetch(sql_query)
                # Convert asyncpg Record objects to standard Python dicts
                return {"status": "success", "data": [dict(r) for r in records]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def execute_write_mutation(
        self, sql_query: str, confirmation_code: str = ""
    ) -> dict:
        """Executes async INSERT, UPDATE, or DELETE SQL mutations.

        Implements Step-Up Authorization for destructive DELETE operations.
        """
        # Step-Up Security Check for DELETE queries
        if "DELETE" in sql_query.upper():
            if confirmation_code != settings.DELETE_CONFIRMATION_SECRET:
                return {
                    "status": "rejected",
                    "message": "Security Violation: Valid confirmation code required for DELETE operations.",
                }

        try:
            pool = await self.get_pool()
            async with pool.acquire() as conn:
                # execute() returns status string like "DELETE 1" or "UPDATE 3"
                status_str = await conn.execute(sql_query)
                rows_affected = status_str.split()[-1] if status_str else "0"
                return {
                    "status": "success",
                    "rows_affected": int(rows_affected) if rows_affected.isdigit() else status_str,
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def close(self):
        """Closes the connection pool on application shutdown."""
        if self.pool:
            await self.pool.close()


# Singleton DB Instance
db = AsyncNeonDB()