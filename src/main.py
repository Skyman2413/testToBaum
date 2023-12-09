import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_session
from models import book_stat
from schemas import InputBook, OutputBook
from tasks import process_book


def create_app():
    app = FastAPI(docs_url='/')

    @app.on_event("startup")
    async def startup_event():
        pass

    @app.post("/add_data")
    async def add_data(book: InputBook, back_tasks: BackgroundTasks,
                       db_conn: AsyncSession = Depends(get_async_db_session)):
        if book.date is None:
            book.date = datetime.datetime.utcnow()
        back_tasks.add_task(process_book, book, db_conn)
        return {"message": "Book in processing"}

    @app.get("/get_data", response_model=List[OutputBook])
    async def get_data(db_conn: AsyncSession = Depends(get_async_db_session)):
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
