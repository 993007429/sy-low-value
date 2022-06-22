"""公厕类型"""
from ninja import Schema


class ToiletTypeIn(Schema):
    name: str


class ToiletTypeOut(Schema):
    id: int
    name: str
