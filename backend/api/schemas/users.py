from pydantic import BaseModel


class UserBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    pass


class UserCreate(UserBase):
    password: str


class UserCreateResponse(UserBase):
    id: int


class User(UserBase):
    id: int
    password: str
