from ninja import Schema


class Login(Schema):
    username: str
    password: str


class Token(Schema):
    username: str
    nickname: str
    phone: str = None
    token: str
    user_id: int = None
