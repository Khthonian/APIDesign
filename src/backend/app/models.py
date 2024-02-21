from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, nullable=False)
    passwordHash = Column(String)
    locations = relationship("Location", back_populates="owner")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    ownerId = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="locations")
