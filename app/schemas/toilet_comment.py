from datetime import datetime
from typing import List

from ninja import Schema

from app.models.comment import ToiletRatingEnum


class ToiletCommentIn(Schema):
    terminal_id: str
    ratings: ToiletRatingEnum
    comment: str = None


class ToiletUserCommentIn(Schema):
    terminal_id: str
    ratings: ToiletRatingEnum
    comment: str = None
    photos: List[str] = []
    anonymous: bool = False


class ToiletCommentOut(Schema):
    id: int
    toilet_id: int
    toilet_name: str
    ratings: int
    comment: str = None
    created_at: datetime
    photos: List[str] = []
    user_id: int = None
    nickname: str = None
