from pydantic import BaseModel


class Token(BaseModel):
    name: str


class TokenData(BaseModel):
    access_token: str
    token_type: str
