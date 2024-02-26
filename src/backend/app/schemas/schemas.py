from typing import List, Optional

from pydantic import BaseModel, EmailStr


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
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    locations: List[int] = []

    class Config:
        orm_mode = True
