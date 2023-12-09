from datetime import datetime

from sqlalchemy import Table, Integer, Column, TIMESTAMP, String, Float, MetaData

metadata = MetaData()

book_stat = Table(
    "book_stat",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", TIMESTAMP, default=datetime.utcnow()),
    Column("title", String, nullable=False),
    Column("x_avg_count_in_line", Float, nullable=False)
)
