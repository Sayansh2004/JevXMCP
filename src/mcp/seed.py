import asyncio
from src.mcp.db import db

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT NOT NULL,
    stories_count INT DEFAULT 0,
    about TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

SAMPLE_USERS = [
    {
        "name": "Alex Rivers",
        "email": "alex.rivers@example.com",
        "age": 28,
        "stories_count": 14,
        "about": "Full-stack engineer interested in distributed systems and AI agents.",
    },
    {
        "name": "Sarah Chen",
        "email": "sarah.chen@example.com",
        "age": 32,
        "stories_count": 8,
        "about": "Tech lead writing about vector search and LLM system reliability.",
    },
    {
        "name": "Marcus Vance",
        "email": "marcus.vance@example.com",
        "age": 24,
        "stories_count": 3,
        "about": "Junior developer exploring Model Context Protocol and FastMCP.",
    },
    {
        "name": "Elena Rostova",
        "email": "elena.rostova@example.com",
        "age": 29,
        "stories_count": 21,
        "about": "AI researcher specializing in sub-100ms non-autoregressive routing.",
    },
    {
        "name": "David Miller",
        "email": "david.miller@example.com",
        "age": 35,
        "stories_count": 0,
        "about": "DevOps engineer monitoring database query performance and security.",
    },
]


async def seed_database():
    """Initializes schema and seeds sample user records into Neon DB."""
    print(" Initializing Neon Database Schema...")

    # 1. Create table
    create_res = await db.execute_write_mutation(CREATE_TABLE_SQL)
    if create_res["status"] == "error":
        print(f"Failed to create table: {create_res['message']}")
        return
    print("Table 'users' verified/created.")

    # 2. Insert sample users
    print("🌱 Seeding sample user records...")
    for user in SAMPLE_USERS:
        insert_sql = f"""
        INSERT INTO users (name, email, age, stories_count, about)
        VALUES (
            '{user["name"]}',
            '{user["email"]}',
            {user["age"]},
            {user["stories_count"]},
            '{user["about"].replace("'", "''")}'
        )
        ON CONFLICT (email) DO NOTHING;
        """
        await db.execute_write_mutation(insert_sql)

    # 3. Verify inserted records
    verification = await db.execute_read_query("SELECT COUNT(*) FROM users;")
    print(f"🎉 Database seeded successfully! Total users in DB: {verification['data'][0]['count']}")

    await db.close()


if __name__ == "__main__":
    asyncio.run(seed_database())