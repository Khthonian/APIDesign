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
    user: str


class UserRefresh(BaseModel):
    user: UserUpdate
    access_token: str
    refresh_token: str


class UserBalance(BaseModel):
    credits: int


class UserAccount(UserBalance):
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


class SuccessMessage(BaseModel):
    message: str


class Token(SuccessMessage):
    access_token: str
    token_type: str
