from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str


class LocationBase(BaseModel):
    city: str
    country: str


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class WeatherRequest(BaseModel):
    location: LocationBase


class Token(BaseModel):
    message: str
    access_token: str
    token_type: str
