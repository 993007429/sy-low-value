from typing import Optional

from pydantic import BaseModel

from app.models.user import WeChatGenderEnum


class WechatLogin(BaseModel):
    code: str


class WechatSession(BaseModel):
    openid: Optional[str]
    session_key: Optional[str]
    unionid: Optional[str]  # noqa
    errcode: Optional[int]
    errmsg: Optional[str]


class WechatUserUpdate(BaseModel):
    nickname: str
    avatar: str
    gender: WeChatGenderEnum
    country: Optional[str]
    province: Optional[str]
    city: Optional[str]


class WechatUserVo(BaseModel):
    nickname: Optional[str]
    avatar: Optional[str]
    gender: WeChatGenderEnum
    country: Optional[str]
    province: Optional[str]
    city: Optional[str]

    class Config:
        orm_mode = True
