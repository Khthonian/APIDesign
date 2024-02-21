from typing import List, Optional

from pydantic import BaseModel


class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    ownerId: Optional[int]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    credits: int = 2000
    username: str
    password: str


class User(UserBase):
    id: int
    locations: List[int] = []

    class Config:
        orm_mode = True
