from typing import Sequence

from pydantic import BaseModel, HttpUrl


class Location(BaseModel):
    id: int
    name: str
    weather: str
    url: str


class LocationSearch(BaseModel):
    response: Sequence[Location]


class LocationCreate(BaseModel):
    idSubmit: int
    name: str
    weather: str
    url: str
