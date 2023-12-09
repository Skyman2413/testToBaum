import asyncio
import datetime
import json

from redis.asyncio import Redis
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import book_stat


async def process_books(redis_conn: Redis, db_conn: AsyncSession):
    while True:
        book = await redis_conn.blpop(['task_queue'], 0)
        data_book = json.loads(book[1])
        x_count = 0
        i = 0
        for line in data_book["text"].split("\n"):
            x_count += str(line).lower().count("х")
            i += 1
        average_x_count = x_count / i
        stmt = insert(book_stat).values(date=data_book["date"], title=data_book["title"],
                                        x_avg_count_in_line=average_x_count)
        await db_conn.execute(stmt)
        await db_conn.commit()
        await asyncio.sleep(3)


async def count_x_in_books():
    pass
