from typing import Generic, List, TypeVar

from pydantic import Field, BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class Pagination(GenericModel, Generic[T]):
    count: int
    results: List[T] = []

    class Config:
        orm_mode = True


class Page(BaseModel):
    page: int = Field(default=1, gt=0)
    page_size: int = Field(default=20, gt=0, le=100)
