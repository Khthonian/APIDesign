from typing import Sequence

from pydantic import BaseModel, HttpUrl


class User(BaseModel):
    id: int
    name: str
    credits: int
    username: str


class UserSearch(BaseModel):
    response: Sequence[User]


class UserCreate(BaseModel):
    name: str
    credits: int
    username: str
