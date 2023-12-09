from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import book_stat
from schemas import InputBook


async def process_book(book: InputBook, db_conn: AsyncSession):
    x_count = 0
    i = 0
    for line in book.text.split("\n"):
        x_count += str(line).lower().count("х")
        i += 1
    average_x_count = x_count / i
    stmt = insert(book_stat).values(date=book.date, title=book.title,
                                    x_avg_count_in_line=average_x_count)
    await db_conn.execute(stmt)
    await db_conn.commit()
