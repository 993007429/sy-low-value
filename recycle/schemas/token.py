from ninja import Schema


class Login(Schema):
    username: str
    password: str


class Token(Schema):
    username: str
    name: str
    token: str
    user_id: int
