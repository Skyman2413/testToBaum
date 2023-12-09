from datetime import datetime
from pydantic import BaseModel


class InputBook(BaseModel):
    date: None | datetime = None
    title: str
    text: str


class OutputBook(BaseModel):
    date: datetime
    title: str
    x_avg_count_in_line: float
