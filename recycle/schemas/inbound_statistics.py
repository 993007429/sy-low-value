from ninja import Schema
from pydantic import Field


class ThroughputOut(Schema):
    throughput: float = Field(0, title="处理量")
