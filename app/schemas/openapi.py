from ninja import Schema
from pydantic import Field


class TicketOut(Schema):
    ticket: str = Field(..., description="一次性免密登录凭证")


class TicketLoginIn(Schema):
    ticket: str
