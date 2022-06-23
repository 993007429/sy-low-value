from typing import Generic, List, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class Pagination(GenericModel, Generic[T]):
    count: int
    results: List[T] = []

    class Config:
        orm_mode = True
