from datetime import datetime
from typing import List, Optional, Union

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


class LocationListing(BaseModel):
    temperature: Optional[float]
    city: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    user_id: Optional[int]
    timestamp: Optional[Union[str, datetime]]
    country: Optional[str]
    id: Optional[int]
    description: Optional[str]


class LocationList(BaseModel):
    locations: List[Optional[LocationListing]]
    pages: int

    class Config:
        arbitrary_types_allowed = True


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
