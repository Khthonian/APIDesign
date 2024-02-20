from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.baseClass import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    credits = Column(Integer, nullable=False)
    username = Column(String(256), nullable=False)
