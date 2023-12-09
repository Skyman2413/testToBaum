import asyncio
import datetime
from contextlib import asynccontextmanager
from typing import List

import redis.asyncio
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_session
from models import book_stat
from redis_config import get_async_redis_client
from schemas import InputBook, OutputBook
from tasks import process_books


def create_app():
    @asynccontextmanager
    async def lifespann(app: FastAPI):
        redis_conn_generator = get_async_redis_client()
        redis_conn = await redis_conn_generator.asend(None)
        db_conn_generator = get_async_db_session()
        db_conn = await db_conn_generator.asend(None)
        asyncio.create_task(process_books(redis_conn=redis_conn, db_conn=db_conn))
        yield
        await redis_conn_generator.aclose()
        await db_conn_generator.aclose()

    app = FastAPI(docs_url='/', lifespan=lifespann)

    @app.on_event("startup")
    async def startup_event():
        pass

    @app.post("/add_data")
    async def add_data(book: InputBook, redis_conn: redis.asyncio.Redis = Depends(get_async_redis_client)):
        if book.date is None:
            book.date = datetime.datetime.utcnow()
        await redis_conn.rpush('task_queue', book.model_dump_json())
        return {"message": "Book in processing"}

    @app.get("/get_data", response_model=List[OutputBook])
    async def get_data(db_conn: AsyncSession = Depends(get_async_db_session)):
        columns = [book_stat.c.date, book_stat.c.title, book_stat.c.x_avg_count_in_line]
        query = select(book_stat)
        result = await db_conn.execute(query)

        return result.all()

    return app


def main():
    uvicorn.run(
        f"{__name__}:create_app",
        host='0.0.0.0', port=8888,
        reload=True
    )


if __name__ == '__main__':
    print("")
    main()
