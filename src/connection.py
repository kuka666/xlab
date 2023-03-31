import asyncpg
import os
from dotenv import load_dotenv

db_pool = None
load_dotenv()


async def get_db_pool():
    global db_pool
    if db_pool is None or db_pool.close():
        db_pool = await asyncpg.create_pool(
            host="db",
            port="5432",
            user="postgres",
            password="dbhec123",
            database="tz"
        )
    return db_pool
